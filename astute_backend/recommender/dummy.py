import uuid

from asgiref.sync import sync_to_async

from .base import Recommender
from ..models import Good


class DummyRecommender(Recommender):
    async def predict(self, real_goods: list) -> list:
        recommended = await self.get_goods(real_goods)
        # recommended = [uuid.uuid4, uuid.uuid4]
        if len(recommended) >= 2:
            return recommended[:2]
        else:
             return []

    @sync_to_async
    def get_goods(self, real_goods):
        return list(Good.objects.all().exclude(id__in=real_goods).values_list('id', flat=True))

