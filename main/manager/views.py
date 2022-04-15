from django.shortcuts import render,redirect
from .models import Rooms,TimeSlot,AdvanceBooking
from .forms import RoomForm,TimeSlotForm,TimeSlotUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from manager.decorators import role_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

@login_required
@role_required(allowed=['manager'])
def manager(request):
    rooms = Rooms.objects.filter(room_owner=request.user)
    advancebooking = AdvanceBooking.objects.get(manager_id=request.user)
    context={'rooms':rooms,'adv_days':advancebooking}
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
            return HttpResponseRedirect(request.path_info)
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
            return HttpResponseRedirect(request.path_info)
        except:
            messages.error(request,'Time Slot Already exist')

    ts = TimeSlot.objects.filter(slot_owner=request.user,
                                  room_id=Rooms.objects.get(id=pk))
    context={'form':form , 'ts':ts}
    return render(request,'manager/add_time_slot.html',context)

@login_required
@role_required(allowed=['manager'])
def editAdvanceDays(request):
    if request.method == "POST":
        days = request.POST["adv_days"]
        user = AdvanceBooking.objects.get(manager_id=request.user)
        user.no_of_days = days
        user.save()
        messages.add_message(request,messages.SUCCESS,'Updated Advance Booking Days')
        return redirect('manager')
    else:
        messages.add_message(request, messages.ERROR, 'Login As Manager.')
        logout(request)
        return redirect("loginPage")

@login_required
@role_required(allowed=['manager'])
def deleteTimeSlot(request,pk1,pk2):
    ts = TimeSlot.objects.get(id=pk2)
    if request.method=="POST":
        print('yes')
        ts.delete()
    success_url = '/manager/create-room/time-slot/' + str(pk1)
    return redirect(success_url)
