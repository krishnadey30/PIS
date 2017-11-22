from django.db import models
from django.utils import timezone
from datetime import datetime 
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from PIL import Image as Img
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The additional attributes we wish to include.
    Phone_no = models.IntegerField(default=0, blank=True)				
    picture = models.ImageField(upload_to='profile_images', blank=True)
    def save(self, *args, **kwargs):
        if self.picture:
            image = Img.open(StringIO.StringIO(self.picture.read()))
            image.thumbnail((200,200), Img.ANTIALIAS)
            output = StringIO.StringIO()
            image.save(output, format='JPEG', quality=75)
            output.seek(0)
            self.picture= InMemoryUploadedFile(output,'ImageField', "cropped_%s" %self.picture.name, 'image/jpeg', output.len, None)
        super(UserProfile, self).save(*args, **kwargs)
    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

class tank(models.Model):
	user_key=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
	longitude=models.FloatField(default=0)
	latitude=models.FloatField(default=0)
	tank_name=models.CharField(max_length=300,blank=True)
	def __str__(self):
		return str(self.tank_name)

class tank_data(models.Model):
	tank_key=models.ForeignKey(tank,on_delete=models.CASCADE)
	time = models.DateTimeField('date published',default=datetime.now, blank=True)
	water_level=models.FloatField(default=0)
	def __str__(self):
		return str(self.water_level)

class ws(models.Model):
	user_key=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
	longitude=models.FloatField(default=0)
	latitude=models.FloatField(default=0)
	location_name=models.CharField(max_length=300)
	def __str__(self):
		return str(self.location_name)

class ws_data(models.Model):
	ws_key=models.ForeignKey(ws,on_delete=models.CASCADE)
	temp=models.FloatField(default=0)    
	humidity=models.FloatField(default=0)
	rainfall=models.FloatField(default=0) 
	time = models.DateTimeField('date published',default=datetime.now, blank=True)
	def __str__(self):
		return str(self.temp)

class plant(models.Model):
	user_key=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
	ws_key=models.ForeignKey(ws)
	tank_key=models.ForeignKey(tank)
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
		return str(self.plant_key.plant_name)

