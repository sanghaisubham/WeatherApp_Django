from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
# Create your views here.
def index(request):

	#url='http://api.openweathermap.org/data/2.5/forecast?id=5506956&APPID=186710ec6275453e7603fa641ec2c659'
	url='http://api.openweathermap.org/data/2.5/weather?q={}&APPID=75f5ac2d07b71628036060ebaa0ac95b'

	weather_data=[]
	if request.method=='POST':
		form=CityForm(request.POST)
		name=request.POST['name']
		if City.objects.filter(name=name).exists():
			print('Already exists')
		else:
			# if (requests.get(url.format(name)).json()).status_code ==200
			if (requests.get(url.format(name))).status_code==200:
				form.save()
	form=CityForm()
	cities=City.objects.all()
	for city in cities:
		r=requests.get(url.format(city)).json() #Json is a combination of python dictionary and Python lists

		city_weather={
		'city':city.name,
		'temperature':r['main']['temp'],
		'description':r['weather'][0]['description'],
		'icon':r['weather'][0]['icon']
		}

		weather_data.append(city_weather)
	
	context={'weather_data':weather_data,'form':form}
	return render(request,'weather/weather.html',context)