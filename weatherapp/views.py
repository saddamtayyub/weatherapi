from django.http.response import HttpResponse
from django.shortcuts import render
import requests
# cache 
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = 1500
# Create your views here.
from django.shortcuts import render
# import json to load json data to python dictionary
import json

def index(request):
	if request.method == 'POST':
		city = request.POST['city']


		# source contain JSON data from API
				
		if f'{city}' in cache:
			data= cache.get(f'{city}')
			print("cache data=========================================")			 	         
			# # data for variable source
		else:
			try:
				source=requests.get('https://api.openweathermap.org/data/2.5/weather?q='+ 
				city + '&appid=194c26cd9195c62fbe92d67cf0d386a4').json()
				data = {
					"location_name":str(source['name']),
					"country_code": str(source['sys']['country']),
					"coordinate": str(source['coord']['lon']) + ' '
								+ str(source['coord']['lat']),
					"temp": str(source['main']['temp']-273.15) + '  °C',
					"pressure": str(source['main']['pressure']),
					"humidity": str(source['main']['humidity']),
				}
				# print(data)
				# cache.set('cachedata', data, timeout=CACHE_TTL)				
				cache.set(f'{city}', data, timeout=CACHE_TTL)
				print("api--- data================================")
			except Exception as e:
				print(e)
				data={
					"location_name":" not valid location",
					"country_code": " ",
					"coordinate":' ',
					"temp":"  ",
					"pressure":'  ',
					"humidity":'  ',
                                                     
				}     
	else:
		data ={}
	return render(request, "index.html",data)

