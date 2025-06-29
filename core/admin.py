from django.contrib import admin
from .models import Master, Order, Service

admin.site.register(Master)
admin.site.register(Order)
admin.site.register(Service)