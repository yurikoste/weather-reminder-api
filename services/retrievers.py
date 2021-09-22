from reminderAPI.models import Weather
from config.settings import WEATHER_API_URL, WEATHER_API_UNITS, WEATHER_API_KEY
import requests


def get_weather_from_server(reminder):
    url = f"{WEATHER_API_URL}?q={reminder.city}&units={WEATHER_API_UNITS}&APPID={WEATHER_API_KEY}"
    request_results = requests.get(url).json()
    if request_results['cod'] == 200:
        weather = Weather.objects.create(
            reminder=reminder,
            temp=request_results['main']['temp'],
            feels_like=request_results['main']['feels_like'],
            pressure=request_results['main']['pressure'],
            wind=request_results['wind']['speed'],
            visibility=request_results['visibility'],
            city=request_results['name']
        )
        return {'response': 'Weather was successfully added to DB', 'weather_obj': weather}
    else:
        return {'response': request_results['cod']}


def update_weather_from_server(reminder):
    url = f"{WEATHER_API_URL}?q={reminder.city}&units={WEATHER_API_UNITS}&APPID={WEATHER_API_KEY}"
    request_results = requests.get(url).json()
    if request_results['cod'] == 200:
        Weather.objects.filter(reminder_id=reminder.pk).update(
            reminder=reminder,
            temp=request_results['main']['temp'],
            feels_like=request_results['main']['feels_like'],
            pressure=request_results['main']['pressure'],
            wind=request_results['wind']['speed'],
            visibility=request_results['visibility'],
            city=request_results['name']
        )
        return {'response': 'Weather was successfully updated in DB'}
    else:
        return {'response': request_results['cod']}
