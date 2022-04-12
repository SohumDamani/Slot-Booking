from django.shortcuts import render
from django.http import HttpResponse

def client(request):
    context={}
    return render(request,'client/client.html',context)

# Create your views here.
