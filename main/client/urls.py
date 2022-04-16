from django.urls import path
from . import views

urlpatterns=[
    path('',views.client,name='client'),
    path('search-time-slot/',views.searchTimeSlot,name='search_result'),
]