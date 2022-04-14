from django.urls import path
from . import views

urlpatterns=[
    path('login/',views.loginPage,name='loginPage'),
    path('logout/',views.logoutPage,name='logoutPage'),
    path('signup/manager',views.ManagerSignUpView,name='manager_signup'),
    path('signup/customer',views.CustomerSignUpView,name='customer_signup'),
]
