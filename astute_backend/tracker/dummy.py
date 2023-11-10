import uuid

from .base import Tracker


class DummyTracker(Tracker):
    def __init__(self, annotations_path: list[str]):
        super().__init__(annotations_path)

    def predict(self, frames, destination_coords: tuple[int]):
        return uuid.uuid4(), (2, 9)
