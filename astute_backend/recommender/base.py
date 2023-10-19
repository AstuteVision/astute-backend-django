from abc import ABC, abstractmethod


class Recommender(ABC):
    @abstractmethod
    def predict(self, real_goods: list):
        """

        :param real_goods:
        :return:
        """
        raise NotImplementedError("Abstract class call!")
