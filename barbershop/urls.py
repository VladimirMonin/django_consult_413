# barbershop/urls.py
from django.contrib import admin
from django.urls import path
from core.views import landing

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", landing),
]
