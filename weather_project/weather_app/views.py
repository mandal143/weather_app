# weather_app/views.py
from django.shortcuts import render, redirect
from .models import City, WeatherData
import requests, json
from django.db.models import F
from django.db.models.functions import TruncHour
from collections import defaultdict
import json


def index(request):
    cities = City.objects.all()
    temperature_data = {}
    weather_data = {}


    for city in cities:
        weather_data_group = WeatherData.objects.filter(city__name=city.name).annotate(hour=TruncHour('timestamp')).values('hour').annotate(temperature=F('temperature')).order_by('hour')
        latest_data = WeatherData.objects.filter(city=city).order_by('-timestamp').first()
        weather_data[city] = latest_data
        city_temperature_data = {}  # Dictionary to store temperature data for the current city
        
        # Fill the temperature data dictionary for the current city
        for data_point in weather_data_group:
            if data_point['hour']== None:
               hour = data_point['hour']
            else:
               hour = data_point['hour'].strftime('%H:%M')  # Format the hour as 'HH:MM'
            temperature = float(data_point['temperature']) 
            city_temperature_data[hour] = temperature
        
        # Add temperature data for the current city to the main dictionary
        temperature_data[city.name] = city_temperature_data

    temperature_data_json = json.dumps(temperature_data) 
    return render(request, 'index.html', {'weather_data': weather_data,'temperature_data': temperature_data_json})

def add_city(request):
    if request.method == 'POST':
        city_name = request.POST.get('city')
        city_data =  City.objects.create(name=city_name)
        API_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name.lower()}&appid=8774a95d7311c58a0e517afa747a79d5"
        API_respone = requests.get(API_url)
        data = API_respone.json()
        temperature = data['main']['temp']
        WeatherData.objects.create(city=city_data, temperature=temperature)
    return redirect('index')

def get_graph_data(request, city_name):
    weather_data = WeatherData.objects.filter(city__name=city_name)
    return redirect('index')

def remove_city(request, city_id):
    city = City.objects.get(id=city_id)
    city.delete()
    return redirect('index')
