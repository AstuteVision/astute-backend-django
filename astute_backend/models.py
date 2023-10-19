from django.db import models

# Create your models here.

class Good(models.Model):

    id = models.UUIDField(primary_key=True)
    name = models.CharField(blank=False, null=False)
    description = models.TextField(blank=True)
    location = models.ForeignKey('Location', null=True, on_delete=models.SET_NULL)
    cost = models.FloatField(null=False)
    comment = models.TextField(blank=True)
    category = models.TextField(blank=True)
    active = models.BooleanField(default=True)

class Location(models.Model):

    id = models.UUIDField(primary_key=True)
    name = models.CharField(null=False, blank=False)
    coordinates_vertical = models.FloatField(null=True, blank=True)
    coordinates_horizontal = models.FloatField(null=True, blank=True)
    location_type = models.ForeignKey('LocationType', null=False, on_delete=models.CASCADE)

class LocationType(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(null=False, blank=False)




