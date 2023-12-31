# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Goods(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(null = False, blank = False)
    description = models.TextField(blank=True)
    coordinates_vertical = models.FloatField(blank=True, )
    coordinates_horizontal = models.FloatField(blank=True)
    cost = models.FloatField(null = False, blank = False)
    comment = models.TextField(blank=True)
    category = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'Goods'
