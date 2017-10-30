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
	all_plants = plant.objects.all()
	final=[]
	for plants in all_plants:
		temp=[]
		temp.append(int(plants.id))
		temp.append(str(plants.plant_name))
		r=plants.tank_key
		SD=soil_data.objects.filter(plant_key=plants)
		x=SD[len(SD)-1].moisture
		temp.append(int(x))
		final.append(temp)
	return render(request,'plants.html',{'all_plants':final})
	
def common(request,plant_id,index):
	index=int(index)
	x=plant.objects.get(id=plant_id)
	r=x.tank_key
	w=x.ws_key
	WSD=ws_data.objects.filter(ws_key=w)
	SD=soil_data.objects.filter(plant_key=x)
	TD=tank_data.objects.filter(tank_key=r)
	if(index<=3):
		obj=WSD
	elif(index==4):
		obj=SD
	temp=[]
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
	return render(request,'common.html',{'temp':temp,'tank':TD,'soil':SD,'weather':WSD,'name':val})
def retrieve(request):
	WaterLevel=request.GET['WaterLevel']
	plantID=request.GET['plantID']
	soilMoisture=request.GET['soilMoisture']
	humidity=request.GET['humidity']
	temperature=request.GET['temperature']
	rainChances=request.GET['rainChances']
	o=get_object_or_404(plant,id=plantID)
	r=o.tank_key
	w=o.ws_key
	s=soil_data(plant_key=o,moisture=soilMoisture)
	s.save()
	t=tank_data(tank_key=r,water_level=WaterLevel)
	t.save()
	W=ws_data(ws_key=w,temp=temperature,humidity=humidity,rainfall=rainChances)
	W.save()
	return HttpResponse("sensor_values")