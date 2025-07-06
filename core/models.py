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
    status = models.CharField(choices=STATUS_CHOICES, default="new", max_length=20, verbose_name="Статус")
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="Дата обновления")
    master = models.ForeignKey("Master", on_delete=models.SET_NULL, null=True, verbose_name="Мастер")
    appointment_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата записи")
    services = models.ManyToManyField("Service", verbose_name="Услуги", default=None, related_name="orders")
    def __str__(self):
        return f"{self.name} - {self.phone}"


class Master(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя")
    photo = models.ImageField(upload_to="masters", verbose_name="Фото", null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(
        null=True, blank=True, max_length=250, verbose_name="Адрес"
    )
    experience = models.PositiveIntegerField(verbose_name="Опыт работы", blank=True, null=True, default=0)
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    services = models.ManyToManyField("Service", verbose_name="Услуги", default=None, related_name="masters")
    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.PositiveIntegerField(
        verbose_name="Длительность", help_text="Время выполнения в минутах", default=30
    )
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")
    image = models.ImageField(
        upload_to="services/", blank=True, verbose_name="Изображение"
    )

    def __str__(self):
        return self.name
