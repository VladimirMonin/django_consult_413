from typing import Any
from django.contrib import admin
from django.db.models import QuerySet, Sum
from .models import Master, Order, Service, Review

admin.site.register(Master)
# admin.site.register(Order)
admin.site.register(Service)


# Делаем фильтр для OrderAdmin total_price
class TotalOrderPrice(admin.SimpleListFilter):
    title = "По общей сумме заказа"
    # total_order_price=one_thousend
    parameter_name = "total_order_price"

    def lookups(self, request, model_admin):
        "Возвращают варианты фильтра"
        return (
            ("one_thousend", "До тысячи"),
            ("three_thousends", "До трех тысяч"),
            ("five_thousends", "До пяти тысяч"),
            ("up_five_thousends", "От пяти тысяч"),
        )

    def queryset(self, request, queryset):
        """
        Возвращает данные в зависимости от нажатой кнопки фильтра
        """
        queryset = queryset.annotate(total_price_agg=Sum("services__price"))

        if self.value() == "one_thousend":
            return queryset.filter(total_price_agg__lt=1000)
        if self.value() == "three_thousends":
            return queryset.filter(total_price_agg__gte=1000, total_price_agg__lt=3000)
        if self.value() == "five_thousends":
            return queryset.filter(total_price_agg__gte=3000, total_price_agg__lt=5000)
        if self.value() == "up_five_thousends":
            return queryset.filter(total_price_agg__gte=5000)

        return queryset


# Делаем красивый вариант для Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    # Отображение полей в списке
    list_display = (
        "name",
        "phone",
        "master",
        "date_created",
        "appointment_date",
        "status",
        "total_price",
        "total_income",
    )

    # Поисковая форма
    search_fields = ("name", "phone", "comment")

    # Фильтрация
    list_filter = ("status", "master", TotalOrderPrice)

    # Сколько записей на странице
    list_per_page = 20

    # Кликабельные поля
    list_display_links = ("phone", "name")

    # Поля, которые можно редактировать
    list_editable = ("status",)

    # НЕ редактируемые поля в детальном просмотре (выводит автонаполняемые поля, убирает возможность редактирования если надо)
    readonly_fields = ("date_created", "date_updated", "total_price", "total_income")

    # Регистрация действий
    actions = ("mark_completed", "mark_canceled", "mark_new", "mark_confirmed")

    # Удобное отоброжение M2M услуг в детальном отображении
    filter_horizontal = ("services",)

    # Группируем поля на странице редактирования
    fieldsets = (
        ("Основная информация", {"fields": ("name", "phone", "status", "comment")}),
        ("Детали записи", {"fields": ("master", "appointment_date", "services")}),
        (
            "Финансовая информация (только для чтения)",
            {
                "classes": ("collapse",),  # Делаем блок сворачиваемым
                "fields": ("total_price", "total_income"),
            },
        ),
        (
            "Служебная информация (только для чтения)",
            {"classes": ("collapse",), "fields": ("date_created", "date_updated")},
        ),
    )

    # Кастомное действие - отметить заявки как completed - Завершена
    @admin.action(description="Отметить как завершенные")
    def mark_completed(self, request, queryset):
        queryset.update(status="completed")

    @admin.action(description="Отметить как отмененные")
    def mark_canceled(self, request, queryset):
        queryset.update(status="canceled")

    @admin.action(description="Отметить как новые")
    def mark_new(self, request, queryset):
        queryset.update(status="new")

    @admin.action(description="Отметить как подтвержденные")
    def mark_confirmed(self, request, queryset):
        queryset.update(status="confirmed")

    # Кастомный столбец с общей суммой M2M services
    @admin.display(description="Общая стоимость")
    def total_price(self, obj):
        return sum([service.price for service in obj.services.all()])

    # Кастомный столбец - сколько денег нам принес этот номер телефона сумма всех услуг всех заказов этого номера со статусом completed
    @admin.display(description="Выручка по номеру")
    def total_income(self, obj):
        # Найти все заявки сделанные с этим номером телефона + статус завершено и жадно выгрузить все услуги
        orders = Order.objects.filter(
            phone=obj.phone, status="completed"
        ).prefetch_related("services")
        # Суммируем все цены услуг
        return sum(
            [service.price for order in orders for service in order.services.all()]
        )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["master", "rating", "status", "created_at"]
    list_filter = ["master", "rating", "status"]
    search_fields = ["master__name", "comment"]
    readonly_fields = ["created_at", "rating"]
    list_editable = ["status"]
    list_per_page = 10
    actions = ["check_published"]

    @admin.action(description="Опубликовать отзыв")
    def check_published(self, request, queryset):
        queryset.update(status="published")
    
    
