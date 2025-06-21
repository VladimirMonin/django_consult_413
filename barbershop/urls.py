# barbershop/urls.py

### Таблица маршрутов, представлений и шаблонов


from django.contrib import admin
from django.urls import path
from core.views import landing, thanks, orders_list, order_detail, test_template

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", landing),
    path("thanks/", thanks),
    path("orders/", orders_list),
    path("orders/<int:order_id>/", order_detail),
    path("test_template/", test_template),
]
