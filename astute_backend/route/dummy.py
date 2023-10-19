from astute_backend.models import Good
from astute_backend.route.base import RouteBuilder


class DummyRouteBuilder(RouteBuilder):

    def __init__(self, real_goods: list, recommendations: list):
        self.route = self.build_route(real_goods, recommendations)
        self.coordinations = self.__find_coords(real_goods, recommendations)

    def build_route(self, real_goods: list, recommended: list):
        return recommended+real_goods

    def __find_coords(self, real_goods: list, recommendations: list):
        coords = {}
        for good in real_goods:
            coords[good] = (1, 1)
        for good in recommendations:
            coords[good] = (1, 1)
        return coords