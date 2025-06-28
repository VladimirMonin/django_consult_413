from django.db import models

class Order(models.Model):
    name = models.CharField()
    phone  = models.CharField()
    comment = models.CharField()