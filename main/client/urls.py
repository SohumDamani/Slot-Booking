from django.urls import path
from . import views

urlpatterns=[
    path('',views.client,name='client'),
    path('search-time-slot/',views.searchTimeSlot,name='search_result'),
    path('booked-slot/', views.bookedSlot, name="booked_slot"),
    path('booked-slot/booked-history/', views.bookedHistory, name="booked_history"),
    path('timeslot/delete/<str:pk>', views.deleteSlot, name="delete_slot"),
]