from django.db import models


class Order(models.Model):
    STATUS_CHOICES = (
        ("new", "Новая"),
        ("confirmed", "Подтвержденная"),
        ("completed", "Завершена"),
        ("canceled", "Отменена"),
    )

    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    comment = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, default="new", max_length=20)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    master = models.ForeignKey("Master", on_delete=models.SET_NULL, null=True)
    appointment_date = models.DateTimeField(null=True, blank=True)



class Master(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя")
    photo = models.ImageField(upload_to="masters", verbose_name="Фото")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(null=True, blank=True, max_length=250, verbose_name="Адрес")
    experience = models.PositiveIntegerField(verbose_name="Опыт работы")
    is_active = models.BooleanField(default=True, verbose_name="Активен")