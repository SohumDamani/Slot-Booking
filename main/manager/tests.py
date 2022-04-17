from datetime import datetime
from django.test import TestCase,SimpleTestCase
from manager.models import Rooms, TimeSlot, AdvanceBooking
from account.models import CustomUser
from django.urls import reverse, resolve
from manager.views import manager,profile


class TestModels(TestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create(
            username='dywane',
            email = 'email@email.com',
            first_name='The',
            last_name = 'Rock',
            phone = '4815267845',
            is_customer=True,
            is_manager=False
        )
        self.room1 = Rooms.objects.create(
            room_owner=self.user1,
            room_name='Room1'
        )
        self.slot1 = TimeSlot.objects.create(
            room_id=self.room1,
            slot_owner=self.user1,
            start_time=datetime.strptime('12:00:00', "%H:%M:%S"),
            end_time=datetime.strptime('3:00:00', '%H:%M:%S'),
        )
        self.advance_book = AdvanceBooking.objects.create(
            manager_id=self.user1,
            no_of_days=10
        )

    def test_room_creation(self):
        self.assertEquals(self.room1.room_owner, self.user1)
        self.assertEquals(self.room1.room_name, 'Room1')

    def test_slot_creation(self):
        self.assertEquals(self.slot1.room_id, self.room1)
        self.assertEquals(self.slot1.slot_owner, self.user1)
        self.assertEquals(self.slot1.start_time, datetime.strptime('12:00:00', "%H:%M:%S"))
        self.assertEquals(self.slot1.end_time, datetime.strptime('3:00:00', "%H:%M:%S"))

    def test_advance_booking(self):
        self.assertEquals(self.advance_book.manager_id, self.user1)
        self.assertEquals(self.advance_book.no_of_days, 10)

class TestUrls(SimpleTestCase):
    def test_manager_home_page(self):
        url = reverse("manager")
        self.assertEquals(resolve(url).func, manager)

    def test_manager_profile(self):
        url = reverse("profile_manager")
        self.assertEquals(resolve(url).func, profile)





