from django.urls import path
from . import views

urlpatterns=[
    path('login/',views.loginPage,name='loginPage'),
    path('logout/',views.logoutPage,name='logoutPage'),
    path('signup/manager',views.managerSignUp,name='manager_signup'),
    path('signup/client',views.clientSignUp,name='client_signup'),
]
