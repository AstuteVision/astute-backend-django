from rest_framework import serializers

from astute_backend.models import Good, Location


class GoodSerializer(serializers.ModelSerializer):
    class Meta():
        model = Good
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta():
        model = Location
        fields = '__all__'
