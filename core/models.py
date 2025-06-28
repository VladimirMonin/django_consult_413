from django.db import models


class Masetr(models.Model):
    name = models.CharField()
    phone = models.CharField()


class Order(models.Model):
    name = models.CharField()
    phone = models.CharField()
    comment = models.CharField()
    master = models.ForeignKey("Master", on_delete=models.SET_NULL, null=True)
