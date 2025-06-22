# barbershop/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from core.views import landing, thanks, orders_list, order_detail


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", landing),
    path("thanks/", thanks),
    path("orders/", orders_list),
    path("orders/<int:order_id>/", order_detail),
    ] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
