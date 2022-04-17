from django.test import TestCase,Client,SimpleTestCase
from account.models import CustomUser
from django.urls import reverse, resolve
from account.views import clientSignUp,managerSignUp,loginPage,logoutPage
from account.forms import UserRegistrationForm

class TestCustomUser(TestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create(
            username='dywane',
            first_name='The',
            last_name='Rock',
            phone='7978797977',
            email='test@gmail.com',
            is_customer=True,
            is_manager=False
        )

    def test_user_creation(self):
        self.assertEquals(self.user1.username, 'dywane')
        self.assertEquals(self.user1.is_customer, True)
        self.assertEquals(self.user1.is_manager, False)

class TestUrls(SimpleTestCase):

    def test_login_is_resolved(self):
        url = reverse('loginPage')
        self.assertEquals(resolve(url).func,loginPage)

    def test_logout_is_resolved(self):
        url = reverse('logoutPage')
        self.assertEquals(resolve(url).func,logoutPage)

    def test_manager_signup_is_resolved(self):
        url = reverse('manager_signup')
        self.assertEquals(resolve(url).func,managerSignUp)

    def test_client_signup_is_resolved(self):
        url = reverse('client_signup')
        self.assertEquals(resolve(url).func,clientSignUp)

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.create_manager = reverse("manager_signup")
        self.create_client = reverse("client_signup")

    def test_login(self):
        self.credentials = {
            'username': 'dywane',
            'password': 'the_rock'
        }
        CustomUser.objects.create_user(**self.credentials)
        response = self.client.post('/account/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_create_manager(self):
        # get request
        response = self.client.get(self.create_manager)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "account/login_registration.html")

        # post request
        response = self.client.post(self.create_manager, {
            'username': 'dywane',
            'email': 'email@email.com',
            'first_name': 'The',
            'last_name': 'Rock',
            'phone': '4815267845',
            'password1': 'the_rock',
            'password2': 'the_rock'
        })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(CustomUser.objects.get(username='dywane').email, 'email@email.com')
        self.assertEquals(CustomUser.objects.get(username='dywane').username, 'dywane')

    def test_create_client(self):
        response = self.client.get(self.create_client)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'account/login_registration.html')

        temp = self.client.post(self.create_client,{
            'username': 'dywane',
            'email': 'email@email.com',
            'first_name': 'The',
            'last_name': 'Rock',
            'phone': '4815267845',
            'password1': 'the_rock',
            'password2': 'the_rock'
        })
        self.assertEquals(CustomUser.objects.get(username='dywane').username,'dywane')
        self.assertEquals(CustomUser.objects.get(username='dywane').email,'email@email.com')

class TestForms(TestCase):

    def test_registration_form(self):
        form = UserRegistrationForm(data={
            'username': 'dywane',
            'email': 'email@email.com',
            'first_name': 'The',
            'last_name': 'Rock',
            'phone': '4815267845',
            'password1': 'the_rock',
            'password2': 'the_rock'
        })
        self.assertTrue(form.is_valid())

    def test_registraion_form_without_phone(self):
        form = UserRegistrationForm(data={
            'username': 'dywane',
            'email': 'email@email.com',
            'first_name': 'The',
            'last_name': 'Rock',
            'password1': 'the_rock',
            'password2': 'the_rock'
        })
        self.assertFalse(form.is_valid())
