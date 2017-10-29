from django.contrib import admin
from . models import plant,soil_data,ws,ws_data,tank_data,tank
# Register your models here.
admin.site.register(plant)
admin.site.register(soil_data)
admin.site.register(tank)
admin.site.register(tank_data)
admin.site.register(ws)
admin.site.register(ws_data)