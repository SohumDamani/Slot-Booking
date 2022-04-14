from django.db import models
from account.models import CustomUser
import uuid

class Rooms(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=10, null=False)

    class Meta:
        unique_together = ('room_owner', 'room_name')

    def __str__(self):
        return self.room_name
    #
    def __unicode__(self):
        pass
