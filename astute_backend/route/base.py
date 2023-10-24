from abc import ABC, abstractmethod


class RouteBuilder(ABC):

    @abstractmethod
    def get_route(self, real_goods: list, recommended: list):
        raise NotImplementedError("Abstract class call!")

