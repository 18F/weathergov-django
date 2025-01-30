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

    return render(request, "weather/point.html", locals())
