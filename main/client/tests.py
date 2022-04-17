from datetime import datetime
from django.test import TestCase,SimpleTestCase
from client.models import TimeSlotBook, TimeSlotCancel
from account.models import CustomUser
from manager.models import Rooms, TimeSlot
from django.urls import resolve,reverse
from client.views import profile,client,searchTimeSlot,bookedSlot,bookedHistory,deleteSlot


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
        self.user2 = CustomUser.objects.create(
            username='therock',
            first_name='Dywane',
            last_name='Johnson',
            phone='487253916',
            email='test@gmail.com',
            is_customer=False,
            is_manager=True
        )
        self.room1 = Rooms.objects.create(
            room_owner=self.user2,
            room_name='Room1'
        )
        self.book_slot = TimeSlotBook.objects.create(
            manager_id=self.user2,
            client_id=self.user1,
            date=datetime.today().date(),
            room_id=self.room1,
            start_time=datetime.strptime('12:00:00', "%H:%M:%S"),
            end_time=datetime.strptime('3:00:00', '%H:%M:%S'),
        )
        self.cancel_slot = TimeSlotCancel.objects.create(
            manager_id=self.user2,
            client_id=self.user1,
            date=datetime.today().date(),
            room_id=self.room1,
            start_time=datetime.strptime('12:00:00', "%H:%M:%S"),
            end_time=datetime.strptime('3:00:00', '%H:%M:%S'),
        )
    #
    def test_slot_book(self):
        self.assertEquals(self.book_slot.manager_id, self.user2)
        self.assertEquals(self.book_slot.client_id, self.user1)
        self.assertEquals(self.book_slot.room_id, self.room1)
        self.assertEquals(self.book_slot.date, datetime.today().date())
        self.assertEquals(self.book_slot.start_time, datetime.strptime('12:00:00', "%H:%M:%S"))
        self.assertEquals(self.book_slot.end_time, datetime.strptime('3:00:00', '%H:%M:%S'))

    def test_slot_cancel(self):
        self.assertEquals(self.cancel_slot.manager_id, self.user2)
        self.assertEquals(self.cancel_slot.client_id, self.user1)
        self.assertEquals(self.cancel_slot.room_id, self.room1)
        self.assertEquals(self.cancel_slot.date, datetime.today().date())
        self.assertEquals(self.cancel_slot.start_time, datetime.strptime('12:00:00', "%H:%M:%S"))
        self.assertEquals(self.cancel_slot.end_time, datetime.strptime('3:00:00', '%H:%M:%S'))

class TestUrls(SimpleTestCase):
    def test_profile(self):
        url = reverse("profile_client")
        self.assertEquals(resolve(url).func, profile)

    def test_client_home_page(self):
        url = reverse("client")
        self.assertEquals(resolve(url).func, client)

    def test_search_result(self):
        url = reverse("search_result")
        self.assertEquals(resolve(url).func,searchTimeSlot)

    def test_booked_history(self):
        url = reverse("booked_history")
        self.assertEquals(resolve(url).func,bookedHistory)

    def test_delete_slot(self):
        url = reverse("delete_slot",args=[1])
        self.assertEquals(resolve(url).func,deleteSlot)

class TestViews(TestCase):
    def setUp(self):
        self.search_slot = reverse("search_result")

    def test_search_case(self):
        # GET method
        response = self.client.get(self.search_slot)
        self.assertEquals(response.status_code, 302)
        # POST method
        response = self.client.post(self.search_slot, {
            'start_time': '19:00:00',
            'end_time': '21:00:00',
            'date': datetime.today().date(),
        })
        self.assertEquals(response.status_code, 302)

