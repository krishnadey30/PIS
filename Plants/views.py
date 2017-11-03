from django.shortcuts import redirect,render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from . models import plant,soil_data,ws,ws_data,tank_data,tank
from . forms import UserForm, UserProfileForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control

def register(request):

    # Like before, get the request's context.
    if request.user.is_authenticated:
		return redirect('plants')
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,'register.html',{'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    # Like before, obtain the context for the user's request.
    if request.user.is_authenticated:
		return redirect('plants')
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request,'login.html', {})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

#@login_required(login_url='/login/')
def index(request):
 	return  render(request, 'index.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
def contact(request):
	return render(request,'contact.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
def about(request):
	return render(request,'about.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
def plants(request):
    u = User.objects.get(username=request.user)
    all_plants = plant.objects.filter(user_key=u.userprofile)
    final=[]
    maps=[]
    for plants in all_plants:
    	temp=[]
    	m=[]
    	m.append(plants.latitude)
    	m.append(plants.longitude)
    	m.append(str(plants.plant_name))
    	temp.append(int(plants.id))
    	temp.append(str(plants.plant_name))
    	r=plants.tank_key
    	SD=soil_data.objects.filter(plant_key=plants)
    	x=SD[len(SD)-1].moisture
    	temp.append(int(x))
    	final.append(temp)
    	maps.append(m)
    return render(request,'plants.html',{'all_plants':final,'maps':maps})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
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
		z=str(x.time)
	    	y.append(z[:len(z)-6])
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

	return render(request,'common.html',{'temp':temp,'tank':TD,'soil':SD,'weather':WSD,'name':val,'obj':obj})
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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
def profile(request):
    context = RequestContext(request)
    context_dict = {}
    u = User.objects.get(username=request.user)
    context_dict['user'] = u
    context_dict['userprofile'] = u.userprofile
    return render(request,'profile.html', context_dict)
