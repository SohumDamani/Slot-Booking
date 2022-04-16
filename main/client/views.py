from django.shortcuts import render,redirect
from client.decorators import role_required
from django.contrib.auth.decorators import login_required
from account.models import CustomUser
from client.models import TimeSlotBook,TimeSlotCancel
from manager.models import TimeSlot,Rooms,AdvanceBooking
from datetime import datetime
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect

@login_required
def profile(request):
    if request.method=="POST":
        user = CustomUser.objects.get(username=request.POST.get('username'))
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.save()
        messages.success(request,"Profile Updated")
        return redirect('profile_client')
    return render(request,'profile.html')

@login_required
def client(request):
    return render(request,'client/client.html')

@login_required
@role_required(allowed=['client'])
def searchTimeSlot(request):
    if request.method=="POST":
        st = request.POST["start_time"]
        et = request.POST["end_time"]
        date = request.POST["date"]
        time_slot = TimeSlot.objects.filter(Q(start_time__contains=st))
        context = {'time_slot':time_slot,'date':date}
        return render(request,"client/search_results.html",context)

@login_required
@role_required(allowed=['client'])
def bookedSlot(request):
    if request.method=="POST":
        room_owner = CustomUser.objects.get(id=request.POST["owner"])
        st = request.POST["start_time"]
        et = request.POST["end_time"]
        room_id = Rooms.objects.get(id=request.POST["room_id"])

        date_requested = str(request.POST["date"])
        day1 = date_requested.replace("-","")
        day1 = datetime.strptime(day1,"%Y%m%d").date()

        date_now = str(datetime.today().date()).strip('')
        day2 = date_now.replace("-","")
        day2 = datetime.strptime(day2,"%Y%m%d").date()
        diff = (day1-day2).days
        print(diff)
        adv_day = AdvanceBooking.objects.get(manager_id=room_owner)
        adv_day = adv_day.no_of_days

        if diff>adv_day>=0:
            try:
                tsb = TimeSlotBook(manager_id=room_owner, client_id=request.user,
                                   date=date_requested,room_id=room_id,
                                   start_time=st,end_time=et)
                tsb.save()
                messages.add_message(request, messages.SUCCESS, f'Time Slot Successfully Booked.')
                return redirect(f'booked-history/')
            except:
                messages.add_message(request, messages.WARNING, 'Time Slot Already Booked.')
                return HttpResponseRedirect(request.path_info)

        else:
            messages.add_message(request,messages.WARNING,f"The manager {str(room_owner.username).title()} requires {adv_day} advance booking.")
            return redirect('client')

    return render(request,'client/booked_slot.html')

@login_required
@role_required(allowed=['client'])
def bookedHistory(request):
    tsb = TimeSlotBook.objects.filter(client_id=request.user)
    tsc = TimeSlotCancel.objects.filter(client_id=request.user)
    context = {'booked':tsb,'canceled':tsc}
    return render(request,'client/booked_history.html',context)

@login_required
@role_required(allowed=['client'])
def deleteSlot(request,pk):
    if request.method=="POST":
        tsb = TimeSlotBook.objects.get(id=pk)
        tsc = TimeSlotCancel(manager_id=tsb.manager_id,client_id=tsb.client_id,room_id=tsb.room_id,
                             date = tsb.date,start_time=tsb.start_time,end_time=tsb.end_time)
        tsc.save()
        tsb.delete()
        messages.add_message(request, messages.SUCCESS, 'Time Slot Cancelled Successfully.')
    return redirect('booked_history')