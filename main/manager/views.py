from django.shortcuts import render
from django.http import HttpResponse

def manager(request):
    context={}
    return render(request,'manager/manager.html',context)
