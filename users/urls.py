# users/urls.py

# Все его маршруты будут доступны с префиксом /users/

from django.urls import path
from .views import (
    CustomRegisterView,
    CustomLoginView,
    CustomLogoutView,
    CustomPasswordChangeView,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)

urlpatterns = [
    path("register/", CustomRegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path(
        "change-password/", CustomPasswordChangeView.as_view(), name="change_password"
    ),
    # Восстановление пароля
    # 1. Форма ввода емейл для сброса пароля
    path("password-reset", CustomPasswordResetView.as_view(), name="password_reset"),
    # 2. Маршрут с сообщением "Загляни в емейл - там ссылка на восстановление пароля"
    path("password-reset/done/", CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    # 3. Маршрут обрабатывающий одноразовую ссылку восстановления пароля из email
    path(
        "reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_link"
    ),
    # 4. Маршрут "Ура, вы прошли испытание выносливостью!"
    path("reset/done/", CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
