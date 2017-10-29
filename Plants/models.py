from django.db import models
from django.utils import timezone
from datetime import datetime 

class tank(models.Model):
	longitude=models.FloatField(default=0)
	latitude=models.FloatField(default=0)
	tank_volume=models.FloatField(default=0)

class tank_data(models.Model):
	tank_key=models.ForeignKey(tank,on_delete=models.CASCADE)
	time = models.DateTimeField('date published',default=datetime.now, blank=True)
	water_level=models.FloatField(default=0)
	def __str__(self):
		return str(self.water_level)

class ws(models.Model):
	longitude=models.FloatField(default=0)
	latitude=models.FloatField(default=0)
	location_name=models.CharField(max_length=300)

class ws_data(models.Model):
	ws_key=models.ForeignKey(ws,on_delete=models.CASCADE)
	temp=models.FloatField(default=0)    
	humidity=models.FloatField(default=0)
	rainfall=models.FloatField(default=0) 
	time = models.DateTimeField('date published',default=datetime.now, blank=True)
	def __str__(self):
		return str(self.temp)

class plant(models.Model):
	ws_key=models.ForeignKey(ws,on_delete=models.CASCADE)
	tank_key=models.ForeignKey(tank,on_delete=models.CASCADE)
	plant_name=models.CharField(max_length=200)
	longitude=models.FloatField(default=0)
	latitude=models.FloatField(default=0)
	def __str__(self):
		return str(self.plant_name)

class soil_data(models.Model):
	plant_key=models.ForeignKey(plant,on_delete=models.CASCADE)
	time = models.DateTimeField('date published',default=datetime.now, blank=True)
	moisture=models.FloatField(default=0)
	def __str__(self):
		return str(self.moisture)

