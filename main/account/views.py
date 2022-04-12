from django.shortcuts import render
from django.http import HttpResponse

def account(request):
    context={}
    return render(request,'account/account.html',context)
# Create your views here.
