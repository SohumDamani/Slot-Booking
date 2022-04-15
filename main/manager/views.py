from django.shortcuts import render,redirect
from .models import Rooms,TimeSlot,AdvanceBooking
from .forms import RoomForm,TimeSlotForm,TimeSlotUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from manager.decorators import role_required

@login_required
@role_required(allowed=['manager'])
def manager(request):
    rooms = Rooms.objects.all()
    timeslot = TimeSlot.objects.all()
    advancebooking = AdvanceBooking.objects.all()
    context={'rooms':rooms,'timeslot':timeslot,'advancebooking':advancebooking}
    return render(request,'manager/manager.html',context)

@login_required
@role_required(allowed=['manager'])
def createRoom(request):
    user = request.user
    form = RoomForm()
    if request.method=="POST":
        form = RoomForm(request.POST)
        form.instance.room_owner = user

        try:
            form.is_valid()
            form.save()
            room = Rooms.objects.last()
            return redirect(f'time-slot/{room.pk}')
        except:
            messages.error(request,"Room Already Exist!")
            return redirect('create_room')
    context={'form':form,'user':user}
    return render(request,'manager/create_room.html',context)

@login_required
@role_required(allowed=['manager'])
def deleteRoom(request,pk):
    room = Rooms.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
    return redirect('manager')

@login_required
@role_required(allowed=['manager'])
def addTimeSlot(request,pk):
    user = request.user
    form = TimeSlotForm()
    if request.method=="POST":
        form = TimeSlotForm(request.POST)
        form.instance.slot_owner = user
        form.instance.room_id = Rooms.objects.get(id=pk)
        try:
            form.is_valid()
            form.save()
            return redirect('manager')
        except:
            messages.error(request,'Time Slot Already exist')
    context={'form':form}
    return render(request,'manager/add_time_slot.html',context)
