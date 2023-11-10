from abc import ABC, abstractmethod


class Tracker(ABC):
    def __init__(self, annotations_path: list[str]):
        pass

    @abstractmethod
    async def predict(self, frames, destination_coords: tuple[int]):
        """

        :param frames:
        :param destination_coords:
        :return:
        """
        raise NotImplementedError("Abstract class call!")
