from django.shortcuts import render
from .models import Rooms


def manager(request):
    rooms = Rooms.objects.all()
    context={'rooms':rooms}
    return render(request,'manager/manager.html',context)
