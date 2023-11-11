import json
import math
from collections import defaultdict
from logging import getLogger
from astute_backend.reid.osnet_reid import reid

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
        self.reid = reid

    def predict(self, frames, destination_coords: tuple[int, int], client_id: int) -> tuple[float, tuple[int, int]]:
        yolo_person_class = 0
        results = self.model.track(frames, persist=True, classes=[yolo_person_class], verbose=False)
        for i, camera_result in enumerate(results):
            boxes = camera_result.boxes.xywh.cpu().tolist()
            if boxes is None or camera_result.boxes.id is None:
                logger.info(f"Camera {i} has no boxes")
                continue
            track_ids = camera_result.boxes.id.int().cpu().tolist()
            for box, track_id in zip(boxes, track_ids):
                x, y, w, h = box
                x_down_left = x - w / 2
                y_down_left = y + h / 2
                if self.reid is not None:
                    cropped_person = frames[i][int(y - h / 2):int(y + h / 2), int(x - w / 2):int(x + w / 2)]
                    track_id = reid.predict(cropped_person)
                if track_id != client_id:
                    continue
                direction_angle = self.estimate_person_direction(track_id, x_down_left, y_down_left)
                if direction_angle is not None:
                    next_x, next_y = x_down_left + 150 * math.cos(direction_angle), y_down_left + 150 * math.sin(
                        direction_angle)
                    next_next_x, next_next_y = x_down_left + 300 * math.cos(
                        direction_angle), y_down_left + 300 * math.sin(direction_angle)
                else:
                    next_x = x_down_left
                    next_y = y_down_left
                    next_next_x = x_down_left
                    next_next_y = y_down_left
                non_warped_x = -1
                non_warped_y = -1
                next_non_warped_x = -1
                next_non_warped_y = -1
                for zone_name, zone_points in self.camera_number2locations[i].items():
                    if cv2.pointPolygonTest(zone_points, (int(x_down_left), int(y_down_left)), False) >= 0:
                        current_zone = zone_name
                        non_warped_x, non_warped_y = map(int, current_zone.split("_"))
                    if cv2.pointPolygonTest(zone_points, (int(next_x), int(next_y)), False) >= 0 or cv2.pointPolygonTest(zone_points, (int(next_next_x), int(next_next_y)), False) >= 0:
                        next_zone = zone_name
                        next_non_warped_x, next_non_warped_y = map(int, next_zone.split("_"))
                non_warped_angle = np.arctan2(next_non_warped_y - non_warped_y, next_non_warped_x - non_warped_x)
                # get angle to rotate (in degress) how many angle we need to rotate to get to the destination coords
                angle_to_rotate = np.rad2deg(non_warped_angle - direction_angle)
                return angle_to_rotate, (non_warped_x, non_warped_y)
        return 0, (-1, -1)

    def predict_next_position(self, track_id, x_down_left, y_down_left):
        track = self.track_history[track_id]
        if len(track) > 1:
            dx = track[-1][0] - track[-2][0]
            dy = track[-1][1] - track[-2][1]
            person_direction_angle = np.arctan2(dy, dx)
            person_velocity = np.sqrt(dx ** 2 + dy ** 2)
            if person_velocity < self.std_velocity_threshold:
                person_velocity = 0
            if person_velocity > 0:
                next_x = x_down_left + person_velocity * math.cos(person_direction_angle)
                next_y = y_down_left + person_velocity * math.sin(person_direction_angle)
                return next_x, next_y
        return x_down_left, y_down_left

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
        return 0
