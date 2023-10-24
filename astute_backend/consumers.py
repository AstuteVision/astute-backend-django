import asyncio
import json
import random
import ast
import uuid

from channels.generic.websocket import AsyncWebsocketConsumer

from astute_backend.recommender.dummy import DummyRecommender
from astute_backend.route.dummy import DummyRouteBuilder
from astute_backend.route.greedy import GreedyRouteBuilder
from astute_backend.tracker.dummy import DummyTracker

CONST_cam_ips = "camera_ips.txt"

def get_urls() -> list[str]:
    with open(CONST_cam_ips) as file:
        streams_addresses = [line.rstrip() for line in file]
    return streams_addresses

class Consumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        id = [item[1] for item in self.scope.get('headers') if item[0] == b'client-id'][0].decode('utf-8')
        print("Received", id)
        await self.accept()

    async def websocket_receive(self, text_data):
        real_goods = [uuid.UUID(str(u)) for u in ast.literal_eval(text_data['text'])]
        tracker = DummyTracker()
        recommender = DummyRecommender()
        recommended = await recommender.predict(real_goods)
        route_builder = GreedyRouteBuilder()
        route, coordinates = await route_builder.get_route(real_goods, recommended)
        next_stop = route[0]
        old_direction = 0
        try:
            while True:
                direction, man_coordinate = tracker.predict(None, destination_coords=(1, 1))
                direction = random.random()*100
                if man_coordinate == coordinates[next_stop]:
                    # if destination in real_goods:
                    if next_stop in real_goods:
                        print(f"NEAR_REAL")
                        await self.send(text_data=json.dumps(
                            {"type": "NEAR_REAL", "content": "Вы дошли до REAL"}))
                    if next_stop in recommended:
                        print(f"NEAR_RECOMMENDED")
                        await self.send(text_data=json.dumps(
                            {"type": "NEAR_RECOMMENDED", "content": "Рядом с Вами RECOMMENDED"}))
                    next_stop += route[route.index(next_stop)+1]
                if direction - old_direction:
                    old_direction = direction
                    await self.send(text_data=json.dumps({"type": "DIRECTION", "content": str(direction)}))
                await asyncio.sleep(1)
        except Exception as e:
            print(e)

    async def websocket_disconnect(self, event):
        pass


