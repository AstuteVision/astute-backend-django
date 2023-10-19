from abc import ABC, abstractmethod


class RouteBuilder(ABC):

    @abstractmethod
    def build_route(self, real_goods: list, recommended: list):
        raise NotImplementedError("Abstract class call!")

