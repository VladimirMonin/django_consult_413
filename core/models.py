from django.db import models


class Master(models.Model):
    name = models.CharField()
    phone = models.CharField()
    services = models.ManyToManyField("Service", related_name='masters')

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField()
    phone = models.CharField()
    comment = models.CharField()
    master = models.ForeignKey("Master", on_delete=models.SET_NULL, null=True, related_name='orders')
    services = models.ManyToManyField("Service", related_name='orders')

    def __str__(self):
        return f'Имя: {self.name}, телефон: {self.phone}'
    

class Service(models.Model):
    name = models.CharField()
    price = models.CharField()

    def __str__(self):
        return f'{self.name} - {self.price}'