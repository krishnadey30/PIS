from django.shortcuts import redirect,render,get_object_or_404
from django.http import HttpResponse
from . models import plant,soil

def index(request):
 	return  render(request, 'index.html')
def contact(request):
	return render(request,'contact.html')
def about(request):
	return render(request,'about.html')
def plants(request):
	all_plants=plant.objects.all()
	return render(request,'plants.html',{'all_plants':all_plants})
def common(request,plant_id):
	x=plant.objects.get(id=plant_id)
	obj=soil.objects.filter(plant_key=x)
	return render(request,'common.html',{'obj':obj})
def retrieve(request):
	WaterLevel=request.GET['WaterLevel']
	plantID=request.GET['plantID']
	soilMoisture=request.GET['soilMoisture']
	humidity=request.GET['humidity']
	temperature=request.GET['temperature']
	rainChances=request.GET['rainChances']
	o=get_object_or_404(plant,id=plantID,temp=temperature,humidity=humidity,rainfall=rainChances,water_level=WaterLevel)
	s=soil(plant_key=o,moisture=soilMoisture)
	s.save()
	return HttpResponse("sensor_values")

