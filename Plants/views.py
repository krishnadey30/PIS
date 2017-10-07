from django.shortcuts import redirect,render,get_object_or_404
from django.http import HttpResponse
from . models import plant,soil,weather_station,water_reservoir

def index(request):
 	return  render(request, 'index.html')
def contact(request):
	return render(request,'contact.html')
def about(request):
	return render(request,'about.html')
def plants(request):
	all_plants=plant.objects.all()
	return render(request,'plants.html',{'all_plants':all_plants})
def retrieve(request):
	WaterLevel=request.GET['WaterLevel']
	plantID=request.GET['plantID']
	soilMoisture=request.GET['soilMoisture']
	humidity=request.GET['humidity']
	temperature=request.GET['temperature']
	rainChances=request.GET['rainChances']
	station_id=request.GET['station_id']
	tank_id=request.GET['tank_id']
	o=get_object_or_404(plant,id=plantID)
	s=soil(plant_key=o,moisture=soilMoisture)
	s.save()
	st=weather_station(temp=temperature,humidity=humidity,rainfall=rainChances,station_no=station_id,plant_key=o)
	st.save()
	wt=water_reservoir(plant_key=o,water_level=WaterLevel,reservoir_no=tank_id)
	wt.save()
	return HttpResponse("sensor_values")

