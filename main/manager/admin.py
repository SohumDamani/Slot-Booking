from django.contrib import admin

from .models import Rooms,TimeSlot,AdvanceBooking

admin.site.register(Rooms)
admin.site.register(TimeSlot)
admin.site.register(AdvanceBooking)
