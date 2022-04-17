from datetime import datetime
from django.test import TestCase,SimpleTestCase,RequestFactory,Client
from manager.models import Rooms, TimeSlot, AdvanceBooking
from account.models import CustomUser
from django.urls import reverse, resolve
from manager.views import manager,profile,createRoom,bookingHistory,\
                          addTimeSlot,deleteRoom,editAdvanceDays,deleteTimeSlot
import uuid
from manager.forms import RoomForm,TimeSlotForm

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

    def test_create_room(self):
        url = reverse("create_room")
        self.assertEquals(resolve(url).func,createRoom)

    def test_delete_room(self):
        url = reverse("delete_room",args=[2])
        self.assertEquals(resolve(url).func,deleteRoom)

    def test_add_time_slot(self):
        url = reverse("time_slot", args=[2])
        self.assertEquals(resolve(url).func,addTimeSlot)

    def test_advance_day_edit(self):
        url = reverse("advance_days")
        self.assertEquals(resolve(url).func,editAdvanceDays)

    def test_delete_time_slot(self):
        url = reverse("delete_slot", args=[2,2])
        self.assertEquals(resolve(url).func,deleteTimeSlot)

    def test_booking_history(self):
        url = reverse("bookings")
        self.assertEquals(resolve(url).func,bookingHistory)

class TestViews(TestCase):

    def setUp(self):
        self.create_room = reverse("create_room")
        self.delete_room = reverse("delete_room", args=[uuid.uuid4()])
        self.delete_time_slot = reverse("delete_slot", args=[1, 2])

        self.client = Client()
        self.request_factory = RequestFactory()
        self.user1 = CustomUser.objects.create_user(username='test', email='test@gmail.com', password='user_1',
                                              is_manager=True)
        self.room1 = Rooms.objects.create(room_owner=self.user1, room_name='room2')
        self.create_time_slot = reverse("time_slot", args=[self.room1.id])

    def test_create_room(self):
        self.client.login(username="test", password="user_1")
        request = self.request_factory.get(self.create_room)
        request.user = self.user1
        self.client.post(self.create_room, {
            'room_owner': request.user,
            'room_name': 'room1'
        })
        room1 = Rooms.objects.get(room_name="room2")
        self.assertEquals(room1.room_name, 'room2')
    #
    def test_delete_room(self):
        self.client.login(username="test", password="user_1")
        request = self.request_factory.get(self.delete_room)
        request.user = self.user1
        Rooms.objects.create(room_owner=request.user, room_name='room1')
        Rooms.objects.get(room_name="room1").delete()
        self.assertEquals(Rooms.objects.count(), 1)

    def test_create_time_slot(self, *args, **kwargs):
        self.client.login(username="test", password="user_1")
        request = self.request_factory.get(self.create_time_slot)
        request.user = self.user1
        data = self.client.post(self.create_time_slot, {
            'slot_owner': request.user,
            'room_id': self.room1,
            'start_time': '05:00:00',
            'end_time': '08:00:00',
        })
        ts = TimeSlot.objects.get(slot_owner=request.user, room_id=self.room1.id)
        self.assertEquals(ts.room_id.id, self.room1.id)
        self.assertEquals(ts.slot_owner, request.user)

    def test_delete_time_slot(self):
        self.client.login(username="test", password="user_1")
        request = self.request_factory.get(self.create_time_slot)
        request.user = self.user1
        data = self.client.post(self.create_time_slot, {
            'slot_owner': request.user,
            'room_id': self.room1,
            'start_time': '05:00:00',
            'end_time': '08:00:00',
        })
        ts = TimeSlot.objects.get(slot_owner=request.user, room_id=self.room1.id)
        self.assertEquals(ts.room_id.id, self.room1.id)
        self.assertEquals(ts.slot_owner, request.user)
        TimeSlot.objects.get(slot_owner=request.user, room_id=self.room1.id).delete()
        self.assertEquals(TimeSlot.objects.count(),0)

class TestForms(TestCase):

    def test_room_form(self):
        form = RoomForm(data={
            'room_name':'Room1'
        })
        self.assertTrue(form.is_valid())

    def test_time_slot_form(self):
        form = TimeSlotForm(data={
            'start_time':'3:00:00',
            'end_time':'5:00:00'
        })
        self.assertTrue(form.is_valid())

    def test_time_slot_with_missing_data(self):
        form = TimeSlotForm(data={
            'start_time':'3:00:00'
        })
        self.assertFalse(form.is_valid())


