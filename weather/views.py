from os import getenv
import requests
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
def index(request):
    return render(request, "weather/index.html", locals())

def point_location(request, lat, lon):
    base_url = getenv("INTEROP_URL")
    url = f"{base_url}/point/{lat}/{lon}"
    r = requests.get(url)
    # TODO: Put some error handling here
    point = r.json()

    # We need to reprocess (filter) some array data in
    # the forecast data in order to display this in the templates
    # properly. In Drupal, we were doing this logic in the
    # template.
    filtered = {
        'times': [],
        'temps': [],
        'feelsLike': []
    }
    point["forecast"]["days"][0]["filtered"] = filtered
    for hour in point["forecast"]["days"][0]["hours"]:
        filtered['times'].append(hour['hour'])
        filtered['temps'].append(hour['temperature']['degF'])
        filtered['feelsLike'].append(hour['apparentTemperature']['degF'])
        
    return render(request, "weather/point.html", locals())
