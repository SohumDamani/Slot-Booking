from django.shortcuts import render,redirect
from client.decorators import role_required
from account.models import CustomUser
from client.models import TimeSlotBook
from manager.models import TimeSlot,Rooms,AdvanceBooking
from django.db.models import Q

def client(request):
    return render(request,'client/client.html')

# def searchTimeSlot(request):
#     st = request.GET["start_time"]
#     et = request.GET["end_time"]
#     date = request.GET["date"]
#     # time_slot = TimeSlot.get_queryset().fliter(start_time=st,end_time=et)
#     # context = {'time_slot':time_slot,'date':date}
#     return render(request,"search_result")