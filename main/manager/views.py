from django.shortcuts import render
from django.http import HttpResponse

def manager(request):
    return HttpResponse("Manager Page")
# Create your views here.
