# barbershop/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import (
    LandingTemplateView,
    ThanksTemplateView,
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    ServicesListView,
    ServiceCreateView,
    ServiceUpdateView,
    OrderUpdateView,
    ReviewCreateView,
    AjaxMasterServicesView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", LandingTemplateView.as_view(), name="landing"),
    path("thanks/<str:source>/", ThanksTemplateView.as_view(), name="thanks"),
    path("orders/", OrderListView.as_view(), name="orders"),
    path("orders/<int:order_id>/", OrderDetailView.as_view(), name="order_detail"),
    path("order/create/", OrderCreateView.as_view(), name="order-create"),
    path("review/create/", ReviewCreateView.as_view(), name="review-create"),
    path("services/", ServicesListView.as_view(), name="services-list"),
    path("service/create/", ServiceCreateView.as_view(), name="service-create"),
    path("service/update/<int:service_id>/", ServiceUpdateView.as_view(), name="service-update"),
    path("order/update/<int:order_id>/", OrderUpdateView.as_view(), name="order-update"),

    # AJAX вью для отдачи массива объектов услуг по ID мастера
    path("ajax/services/<int:master_id>/", AjaxMasterServicesView.as_view(), name="get_services_by_master"),

    # Подключаем маршруты приложения users
    path("users/", include("users.urls")),
]

# Добавляем Статику и Медиа ЕСЛИ в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Статика обрабатывается автоматически при DEBUG=True; ручная маршрутизация не требуется
    # Подключим Django Debug Toolbar
    urlpatterns += debug_toolbar_urls()
