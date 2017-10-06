from django.db import models
from django.utils import timezone
from datetime import datetime 
class plant(models.Model):
	plant_name=models.CharField(max_length=200)
	longitude=models.FloatField(default=0)
	latitude=models.FloatField(default=0)
	def __str__(self):
		return str(self.plant_name)

class soil(models.Model):
	plant_key=models.ForeignKey(plant,on_delete=models.CASCADE)
	time = models.DateTimeField('date published',default=datetime.now, blank=True)
	moisture=models.FloatField(default=0)
	def __str__(self):
		return str(self.moisture)
class weather_station(models.Model):
	plant_key=models.ForeignKey(plant,on_delete=models.CASCADE)
	time = models.DateTimeField('date published',default=datetime.now, blank=True)
	temp=models.FloatField(default=0)
	humidity=models.FloatField(default=0)
	rainfall=models.FloatField(default=0)
	station_no=models.IntegerField(default=0)

class water_reservoir(models.Model):
	plant_key=models.ForeignKey(plant,on_delete=models.CASCADE)
	time = models.DateTimeField('date published',default=datetime.now, blank=True)
	water_level=models.FloatField(default=0)
	reservoir_no=models.IntegerField(default=0)