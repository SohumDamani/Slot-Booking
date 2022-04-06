from django.shortcuts import render
from django.http import HttpResponse

def client(request):
    return HttpResponse("Client Page")

# Create your views here.
