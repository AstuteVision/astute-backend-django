import uuid

from asgiref.sync import sync_to_async

from astute_backend.models import Good, Location
from astute_backend.route.base import RouteBuilder


class GreedyRouteBuilder(RouteBuilder):

    async def get_route(self, real_goods: list, recommended: list):
        coordinates = await self.__find_coords(real_goods, recommended)
        box_office = await self.__get_box_office()
        box_office = (box_office['coordinates_vertical'], box_office['coordinates_horizontal'])
        for coord in coordinates:
            coordinates[coord] = (coordinates[coord]['coordinates_vertical'], coordinates[coord]['coordinates_horizontal'])
        route = self.__build_route(real_goods, box_office, coordinates)
        return route, coordinates

    def __build_route(self, real_goods: list, box_office: tuple, coordinates: dict):
        route = []
        route.append(self.__find_min_distance(real_goods, box_office, coordinates, route, False))
        while len(route)<len(coordinates):
            route.append(self.__find_min_distance(real_goods, coordinates[route[-1]], coordinates, route))
        return route[::-1]

    def __find_min_distance(self, real_goods: list, current_point: tuple, coordinates: dict, current_route: list, include_recommended=True):
        min_distance = float('inf')
        next_point = current_point
        for coordinate in coordinates:
            if (current_point[0]-coordinates[coordinate][0])**2+(current_point[1]-coordinates[coordinate][1])**2<min_distance and coordinate not in current_route and (not include_recommended and coordinate in real_goods or include_recommended):
                min_distance = (current_point[0]-coordinates[coordinate][0])**2+(current_point[1]-coordinates[coordinate][1])**2
                next_point = coordinate
        return next_point



    async def __find_coords(self, real_goods: list, recommendations: list):
        coords = {}
        for good in real_goods:
            coords[good] = await self.__get_by_id(good)
        for good in recommendations:
            coords[good] = await self.__get_by_id(good)
        return coords

    @sync_to_async
    def __get_by_id(self, good):
        return list(Location.objects.all().filter(id = list(Good.objects.all().filter(id = good).values())[0]['location_id']).values())[0]

    @sync_to_async
    def __get_box_office(self):
        return list(Location.objects.all().filter(name="Касса").values())[0]

