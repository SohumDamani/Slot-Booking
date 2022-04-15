from django.urls import path
from . import views

urlpatterns = [
    path('',views.manager,name='manager'),
    path('create-room/',views.createRoom,name='create_room'),
    path('create-room/time-slot/<str:pk>/',views.addTimeSlot,name='time_slot'),
    path('room-delete/<str:pk>/',views.deleteRoom,name='delete_room'),
]