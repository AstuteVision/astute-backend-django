import uuid

from .base import Tracker


class DummyTracker(Tracker):
    def predict(self, frames, destination_coords: tuple[int]):
        return uuid.uuid4(), (2, 9)
