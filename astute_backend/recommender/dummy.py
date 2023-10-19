import uuid

from asgiref.sync import sync_to_async

from .base import Recommender
from ..models import Good


class DummyRecommender(Recommender):
    async def predict(self, real_goods: list) -> list:
        goods = await sync_to_async(Good.objects.all)()
        recommended = [good for good in goods if good.id not in real_goods]
        # recommended = [uuid.uuid4, uuid.uuid4]
        if len(goods) >= 2:
            return recommended[:2]
        else:
             return []

