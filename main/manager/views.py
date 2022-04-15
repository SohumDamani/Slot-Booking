from django.shortcuts import render,redirect
from .models import Rooms,TimeSlot,AdvanceBooking
from .forms import RoomForm,TimeSlotForm
from django.contrib import messages


def manager(request):
    rooms = Rooms.objects.all()
    timeslot = TimeSlot.objects.all()
    advancebooking = AdvanceBooking.objects.all()
    context={'rooms':rooms,'timeslot':timeslot,'advancebooking':advancebooking}
    return render(request,'manager/manager.html',context)

def createRoom(request):
    user = request.user
    print("Username : ",user)
    form = RoomForm()
    if request.method=="POST":
        form = RoomForm(request.POST)
        form.instance.room_owner = user
        try:
            form.is_valid()
            form.save()
            return redirect('manager')
        except:
            messages.error(request,"Room Already Exist!")
            return redirect('create_room')
    context={'form':form,'user':user}
    return render(request,'manager/create_room.html',context)

# def updateRoom(request,pk):
#     room = Rooms.objects.get(id=pk)
#     context={}
#     return render(request,'manager/edit-room.html',context)

def addTimeSlot(request,pk):
    user = request.user
    form = TimeSlotForm()
    context={'form':form}
    return render(request,'manager/add_time_slot.html',context)
