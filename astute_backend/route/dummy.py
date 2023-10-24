from astute_backend.models import Good
from astute_backend.route.base import RouteBuilder


class DummyRouteBuilder(RouteBuilder):


    async def get_route(self, real_goods: list, recommended: list):
        return recommended+real_goods, await self.__find_coords(real_goods, recommended)

    async def __find_coords(self, real_goods: list, recommendations: list):
        coords = {}
        for good in real_goods:
            coords[good] = (1, 1)
        for good in recommendations:
            coords[good] = (1, 1)
        return coords