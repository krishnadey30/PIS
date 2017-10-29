from django.shortcuts import redirect,render,get_object_or_404
from django.http import HttpResponse
from . models import plant,soil_data,ws,ws_data,tank_data,tank

def index(request):
 	return  render(request, 'index.html')
def contact(request):
	return render(request,'contact.html')
def about(request):
	return render(request,'about.html')
def plants(request):
	all_plants=plant.objects.all()
	return render(request,'plants.html',{'all_plants':all_plants})
def common(request,plant_id,index):
	x=plant.objects.get(id=plant_id)
	obj=soil.objects.filter(plant_key=x)
	temp=[]
	index=int(index)
	val=""
	for x in obj:
		y=[]
		y.append(str(x.time))
		if(index==1):
			val="Temp"
			y.append(x.temp)
		elif(index==2):
			val="Humidity"
			y.append(x.humidity)
		elif(index==3):
			val="Rainfall"
			y.append(x.rainfall)
		elif(index==4):
			val="Moisture"
			y.append(x.moisture)
		temp.append(y)
	return render(request,'common.html',{'temp':temp,'obj':obj,'name':val})
def retrieve(request):
	WaterLevel=request.GET['WaterLevel']
	plantID=request.GET['plantID']
	soilMoisture=request.GET['soilMoisture']
	humidity=request.GET['humidity']
	temperature=request.GET['temperature']
	rainChances=request.GET['rainChances']
	o=get_object_or_404(plant,id=plantID)
	s=soil(plant_key=o,moisture=soilMoisture,temp=temperature,humidity=humidity,rainfall=rainChances,water_level=WaterLevel)
	s.save()
	return HttpResponse("sensor_values")