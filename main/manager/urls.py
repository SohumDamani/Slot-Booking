from django.urls import path
from . import views

urlpatterns = [
    path('',views.manager,name='manager'),
    path('profile/',views.profile,name='profile_manager'),
    path('create-room/',views.createRoom,name='create_room'),
    path('create-room/time-slot/<str:pk>/',views.addTimeSlot,name='time_slot'),
    path('room-delete/<str:pk>/',views.deleteRoom,name='delete_room'),
    path('advance_days/', views.editAdvanceDays, name="advance_days"),
    path('room/<str:pk1>/delete-time-slot/<str:pk2>', views.deleteTimeSlot, name="delete_slot"),
    path('view-bookings/',views.bookingHistory,name="bookings")
]