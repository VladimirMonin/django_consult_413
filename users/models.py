# users/mode
from django.db import models

# Импорт AbstractUser
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя.
    Наследуясь от AbstractUser мы получаем все его поля и методы
    И можем быть интегрированы в Django гармонично
    """

    avatar = models.ImageField(
        upload_to="avatars", verbose_name="Аватар", null=True, blank=True
    )
    phone = models.CharField(
        max_length=20, verbose_name="Телефон", null=True, blank=True
    )
    birthday = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    vk_id = models.CharField(
        max_length=100, verbose_name="ID пользователя ВКонтакте", null=True, blank=True
    )
    tg_id = models.CharField(
        max_length=100, verbose_name="ID пользователя в Телеграм", null=True, blank=True
    )
