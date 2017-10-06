from django.contrib import admin
from . models import plant,soil,weather_station,water_reservoir
# Register your models here.
admin.site.register(plant)
admin.site.register(soil)
admin.site.register(weather_station)
admin.site.register(water_reservoir)
