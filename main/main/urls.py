from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('client/',include('client.urls')),
    path('manager/',include('manager.urls')),
    path('account/',include('account.urls')),
]
