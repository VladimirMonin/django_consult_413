# barbershop/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import (
    landing,
    thanks,
    orders_list,
    order_detail,
    order_create,
    services_list,
    order_page,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", landing, name="landing"),
    path("thanks/", thanks, name="thanks"),
    path("orders/", orders_list, name="orders"),
    path("orders/<int:order_id>/", order_detail, name="order_detail"),
    path("order/create/", order_create, name="order-create"),
    path("services/", services_list, name="services-list"),
    path("order/", order_page, name="order-page"),
]

# Добавляем Статику и Медиа ЕСЛИ в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]
    )
    # Подключим Django Debug  Toolbar
    urlpatterns += debug_toolbar_urls()
