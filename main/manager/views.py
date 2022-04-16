from django.shortcuts import render,redirect
from .models import Rooms,TimeSlot,AdvanceBooking
from .forms import RoomForm,TimeSlotForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from manager.decorators import role_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from client.models import TimeSlotBook
from django.urls import reverse
from account.models import CustomUser

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
            temp = form.save(commit=False)
            temp.room_name=temp.room_name.title()
            t1 = temp.id
            temp.save()
            return redirect(f'time-slot/{t1}')
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
    room_name = Rooms.objects.get(id=pk)
    if request.method=="POST":
        form = TimeSlotForm(request.POST)
        form.instance.slot_owner = user
        form.instance.room_id = Rooms.objects.get(id=pk)
        temp = form.save(commit=False)
        ts = TimeSlot.objects.filter(room_id=pk)
        client = [str(temp.start_time),str(temp.end_time)]
        print("Client :",client)
        flag=True
        msg = "Time Slot Added Successfully"
        if client[0]>client[1]:
            messages.warning(request,"Start time cannot exceed end time!")
        else:
            for i in ts:
                check=list(str(i).split('-'))
                if client[0]==check[0] and client[1]==check[1]:
                    flag=False
                    msg = "Time Slot Already Added"
                    break
                elif check[0]<client[0]<check[1] or check[0]<client[1]<check[1]:
                    flag=False
                    msg = f"Time slot {'-'.join(client)} clashes with {i}"
                    break
            if flag:
                temp.save()
                messages.success(request,msg)
            else:
                messages.warning(request,msg)

        return redirect(request.path_info)


    ts = TimeSlot.objects.filter(slot_owner=request.user,
                                  room_id=Rooms.objects.get(id=pk))
    context={'form':form , 'ts':ts,'room_name':room_name}
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
    if request.method=="POST":
        ts = TimeSlot.objects.get(id=request.POST.get('slot_id'))
        ts.delete()
        messages.success(request,f"Slot Deleted Successfully ")

    return redirect('manager')
@login_required
@role_required(allowed=['manager'])
def bookingHistory(request):
    tsb = TimeSlotBook.objects.filter(manager_id=request.user)
    context={'bookings':tsb}
    return render(request,'manager/booking_history.html',context)
