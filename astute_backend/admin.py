from django.contrib import admin

import astute_backend
from astute_backend.models import Good, Location, LocationType

# Register your models here.

admin.site.register(Good)
admin.site.register(Location)
admin.site.register(LocationType)
