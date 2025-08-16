# users/urls.py

# Все его маршруты будут доступны с префиксом /users/

from django.urls import path
from .views import CustomRegisterView, CustomLoginView, CustomLogoutView, CustomPasswordChangeView

urlpatterns = [
    path("register/", CustomRegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("change-password/", CustomPasswordChangeView.as_view(), name="change-password")
]
