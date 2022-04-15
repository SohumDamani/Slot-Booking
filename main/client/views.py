from django.shortcuts import render
from django.http import HttpResponse
from client.decorators import role_required

def client(request):
    context={}
    return render(request,'client/client.html',context)

# Create your views here.
