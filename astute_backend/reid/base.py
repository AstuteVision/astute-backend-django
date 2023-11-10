from abc import ABC, abstractmethod


class ReId(ABC):
    @abstractmethod
    def predict(self, cropped_image):
        raise NotImplementedError("Abstract class call!")
