import uuid

from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from astute_backend.models import Good
from astute_backend.serializers import GoodSerializer


# Create your views here.

class GoodApiView(generics.ListAPIView):
    def get(self, request):
        goods = Good.objects.all().filter(active=True).values()
        return Response(list(goods))

class GoodDetailView(generics.RetrieveAPIView):
    queryset = Good.objects.filter(active=True).all()
    serializer_class = GoodSerializer

class UserIdView(generics.ListAPIView):

    def post(self, request):
        id = uuid.uuid4()
        return Response({'id': id})

    # queryset = Good.objects.all()
    # serializer_class = GoodSerializer

