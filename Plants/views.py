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
		return redirect('dashboard')
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
		return redirect('dashboard')
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
def addplant(request):
	context = RequestContext(request)
	if request.method == 'POST':
		plant_name = request.POST['name']
		tank_id = request.POST['tank_id']
		ws_id = request.POST['ws_id']
		wsd=get_object_or_404(ws,id=ws_id)
		tankd=get_object_or_404(tank,id=tank_id)
		u = User.objects.get(username=request.user)
		obj=plant(user_key=u.userprofile,ws_key=wsd,tank_key=tankd,plant_name=plant_name)
		obj.save()
	return HttpResponseRedirect('/dashboard')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')


def index(request):
 	return  render(request, 'index.html')

def retrieve(request):
	WaterLevel=request.GET['WaterLevel']
	plantIDa=request.GET['plantIDa']
	plantIDb=request.GET['plantIDb']
	soilMoisturea=request.GET['soilMoisturea']
	soilMoistureb=request.GET['soilMoistureb']
	humidity=request.GET['humidity']
	temperature=request.GET['temperature']
	rainChances=request.GET['rainChances']
	p1=get_object_or_404(plant,id=plantIDa)
	p2=get_object_or_404(plant,id=plantIDb)
	r=p1.tank_key
	w=p2.ws_key
	s=soil_data(plant_key=p1,moisture=soilMoisturea)
	s.save()
	s=soil_data(plant_key=p2,moisture=soilMoistureb)
	s.save()
	t=tank_data(tank_key=r,water_level=WaterLevel)
	t.save()
	W=ws_data(ws_key=w,temp=temperature,humidity=humidity,rainfall=rainChances)
	W.save()
	return HttpResponse("sensor_values")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/')
def profile(request):
	context_dict={}
	u = User.objects.get(username=request.user)
	all_plants = plant.objects.filter(user_key=u.userprofile)
	tanks = tank.objects.filter(user_key=u.userprofile)
	context_dict['user'] = u
	context_dict['userprofile'] = u.userprofile
	context_dict['all_plants']=all_plants
	context_dict['tank_all']=tanks
	maps=[]
	for plants in all_plants:
		m=[]
		m.append(plants.latitude)
		m.append(plants.longitude)
		m.append(str(plants.plant_name))
		maps.append(m)
	context_dict['maps_plants'] = maps
	maps=[]
	for tank_s in tanks:
		m=[]
		m.append(tank_s.latitude)
		m.append(tank_s.longitude)
		m.append("Tank"+str(tank_s.id))
		maps.append(m)
	context_dict['maps_tanks'] = maps
	context_dict['soil_moisture'] = {}
	for plants in all_plants:
		SD=soil_data.objects.filter(plant_key=plants)
		temp=[]
		for x in SD:
			y=[]
			z=str(x.time)
		    	y.append(z[:len(z)-6])
			y.append(x.moisture)
			temp.append(y)
		context_dict['soil_moisture'][plants.id]=temp
	context_dict['humidity'] = {}
	context_dict['temperature'] = {}
	context_dict['rainfall'] = {}
	for plants in all_plants:
		x=plants
		w=x.ws_key
		WSD=ws_data.objects.filter(ws_key=w)
		humid=[]
		temp=[]
		rain=[]
		for x in WSD:
			y=[]
			a=[]
			b=[]
			z=str(x.time)
		    	y.append(z[:len(z)-6])
			y.append(x.humidity)
			a.append(z[:len(z)-6])
			a.append(x.temp)
			b.append(z[:len(z)-6])
			b.append(x.rainfall)
			temp.append(a)
			humid.append(y)
			rain.append(b)
		context_dict['humidity'][plants.id]=humid
		context_dict['temperature'][plants.id]=temp
		context_dict['rainfall'][plants.id]=rain
	context_dict['tanks'] = {}
	for each_tank in tanks:
		tank_d=tank_data.objects.filter(tank_key=each_tank)
		data=[]
		for x in tank_d:
			y=[]
			z=str(x.time)
		    	y.append(z[:len(z)-6])
			y.append(x.water_level)
			data.append(y)
		context_dict['tanks'][each_tank.id]=data
	return render(request,'dashboard.html', context_dict)

	
