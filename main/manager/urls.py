from django.urls import path
from . import views

urlpatterns = [
    path('',views.manager,name='manager'),
    path('create-room/',views.createRoom,name='create_room'),
    path('time-slot/<str:pk>/',views.addTimeSlot,name='time_slot'),
]