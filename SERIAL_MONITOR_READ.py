import serial
import requests

value=[]
serdata = 0
ser = serial.Serial('COM10',9600)
while True:
	#reading data from serial monitor
    serdata = str(ser.readline())
    serdata = ''.join(x for x in serdata if x.isalnum())
    value.append(serdata)
    
    if(len(value)==5): 
    	#creating url
        print value
        url='http://10.0.3.23:9000/retrieve/?temperature='+str(value[1])+'&humidity='+str(value[0])+'&soilMoisture='+str(value[3])+'&WaterLevel='+str(value[2])+'&rainChances='+str(value[4])+'&plantID='+str(1)
        data = {}
        try:
        	#pulling post request
            requests.post(url,data=data)
        except:
            print("Failed")
        #emptying the arduino data list
        del value[:]
