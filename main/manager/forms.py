from django.forms import ModelForm
from .models import Rooms,TimeSlot


class RoomForm(ModelForm):
    class Meta:
        model = Rooms
        fields = ('room_name', )

class TimeSlotForm(ModelForm):
    class Meta:
        model = TimeSlot
        fields = ('start_time', 'end_time',)



