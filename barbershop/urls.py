# barbershop/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import (
    landing,
    ThanksTemplateView,
    orders_list,
    order_detail,
    order_create,
    services_list,
    service_create,
    service_update,
    order_update,
    review_create,
    get_services_by_master,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", landing, name="landing"),
    path("thanks/<str:source>/", ThanksTemplateView.as_view(), name="thanks"),
    path("orders/", orders_list, name="orders"),
    path("orders/<int:order_id>/", order_detail, name="order_detail"),
    path("order/create/", order_create, name="order-create"),
    path("review/create/", review_create, name="review-create"),
    path("services/", services_list, name="services-list"),
    path("service/create/", service_create, name="service-create"),
    path("service/update/<int:service_id>/", service_update, name="service-update"),
    path("order/update/<int:order_id>/", order_update, name="order-update"),

    # AJAX вью для отдачи массива объектов услуг по ID мастера
    path("ajax/services/<int:master_id>/", get_services_by_master, name="get_services_by_master"),
]

# Добавляем Статику и Медиа ЕСЛИ в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]
    )
    # Подключим Django Debug  Toolbar
    urlpatterns += debug_toolbar_urls()
