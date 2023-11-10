import json
from collections import defaultdict
from logging import getLogger

import cv2
import numpy as np
from ultralytics import YOLO

from .base import Tracker

logger = getLogger(__name__)


def open_annotations(path_to_annotations):
    with open(path_to_annotations) as file:
        zones_json = json.load(file)
        return {shape["label"]: np.array(shape["points"], dtype=np.int32) for shape in zones_json["shapes"]}


class YoloTracker(Tracker):
    def __init__(self, annotation_paths: list[str], yolo_version: str = "yolov8n.pt", max_track_length: int = 30,
                 min_track_length: int = 2, std_velocity_threshold: float = 1.3):
        super().__init__(annotation_paths)
        self.min_track_length = min_track_length
        self.max_track_length = max_track_length
        self.std_velocity_threshold = std_velocity_threshold
        self.camera_number2locations = [open_annotations(path) for path in annotation_paths]
        self.model = YOLO(yolo_version)
        self.track_history = defaultdict(lambda: [])

    def predict(self, frames, destination_coords: tuple[int, int]) -> tuple[float, tuple[int, int]]:
        yolo_person_class = 0
        results = self.model.track(frames, persist=True, classes=[yolo_person_class])
        for i, camera_result in enumerate(results):
            boxes = camera_result.boxes.xywh.cpu().tolist()
            if boxes is None or camera_result.boxes.id is None:
                logger.debug(f"Camera {i} has no boxes")
                continue
            track_ids = camera_result.boxes.id.int().cpu().tolist()
            for box, track_id in zip(boxes, track_ids):
                x, y, w, h = box
                x_down_left = x - w / 2
                y_down_left = y - h / 2
                person_direction = self.estimate_person_direction(track_id, x_down_left, y_down_left)
                for zone_name, zone_points in self.camera_number2locations[i].items():
                    if cv2.pointPolygonTest(zone_points, (int(x), int(y)), False) >= 0:
                        current_zone = zone_name
                        logger.debug(f"Track is in zone {current_zone}")
                    next_point = (int(x + 2 * 60 * np.cos(person_direction)), int(y + 2 * 60 * np.sin(person_direction)))
                    if cv2.pointPolygonTest(zone_points, next_point, False) >= 0:
                        next_zone = zone_name
                        logger.debug(f"Track will be in zone {next_zone}")

        return 0, (-1, -1)

    def estimate_person_direction(self, track_id, x_down_left, y_down_left):
        track = self.track_history[track_id]
        track.append((float(x_down_left), float(y_down_left)))
        if len(track) > self.max_track_length:
            track.pop(0)
        if len(track) > self.min_track_length:
            dx = track[-1][0] - track[-2][0]
            dy = track[-1][1] - track[-2][1]
            person_direction = np.arctan2(dy, dx)
            person_velocity = np.sqrt(dx ** 2 + dy ** 2)
            if person_velocity < self.std_velocity_threshold:
                person_velocity = 0
            if person_velocity > 0:
                return person_direction
        return None, None

    def predict_for_one_camera(self, frames, destination_coords: tuple[int]) -> tuple[float, tuple[int, int]]:
        results = self.model.track(frames[0], persist=True, classes=[0])
        if not results:
            return 0, (-1, -1)
        boxes = results[0].boxes.xywh.cpu().tolist()
        # fixme predict without registration - track only the first one
        if not boxes:
            return 0, (-1, -1)
        box = boxes[0]
        direction = self.__estimate_non_warped_direction(box)
        current_zone_name, next_zone_name = self.__estimate_neigborhood_zones(box, direction=direction)
        if current_zone_name is None:
            return 0, (-2, -2)
        # fixme: zone name must be the coordinates of the center of the zone
        x_current, y_current = map(int, current_zone_name.split(","))
        if next_zone_name is None:
            return 0, (x_current, y_current)
        x_next, y_next = map(int, next_zone_name.split(","))
        dx = x_next - x_current
        dy = y_next - y_current

        x = destination_coords[0] - x_next
        y = destination_coords[1] - y_next

        x_sum = dx+x
        y_sum = dy+y

        angle_to_rotate = np.rad2deg(np.arctan2(y_sum, x_sum))
        print("YOLO", x_current, y_current, "Next", x_next, y_next, "Angle", angle_to_rotate)
        return int(angle_to_rotate), (x_current, y_current)

    def __estimate_neigborhood_zones(self, box, direction):
        x, y, w, h = box
        current_zone = None
        next_zone = None
        for zone_name, zone_points in self.zones.items():
            if cv2.pointPolygonTest(zone_points, (int(x), int(y)), False) >= 0:
                current_zone = zone_name
                logger.debug(f"Track is in zone {zone_name}")
            next_point = (int(x + 2 * 60 * np.cos(direction)), int(y + 2 * 60 * np.sin(direction)))
            if cv2.pointPolygonTest(zone_points, next_point, False) >= 0:
                next_zone = zone_name
                logger.debug(f"Track will be in zone {zone_name}")
        return current_zone, next_zone
