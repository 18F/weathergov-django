from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "weather/index.html", locals())

def point_location(request, lat, lon):
    return render(request, "weather/point.html", locals())
