# core/context_processors.py
from django.urls import reverse


def menu_items(request):
    """
    Контекстный процессор для добавления меню в контекст шаблонов.
    """
    menu = [
        {
            "name": "Главная",
            "url": reverse("landing") + "#top",
            "icon_class": "bi-house",
        },
        {
            "name": "Мастера",
            "url": reverse("landing") + "#masters",
            "icon_class": "bi-person-badge",
        },
        {
            "name": "Услуги",
            "url": reverse("landing") + "#services",
            "icon_class": "bi-scissors",
        },
        {
            "name": "Отзывы",
            "url": reverse("landing") + "#reviews",
            "icon_class": "bi-chat-dots",
        },
        {
            "name": "Записаться",
            "url": reverse("landing") + "#get-order",
            "icon_class": "bi-calendar-check",
        },
    ]

    staff_menu = [
        {
            "name": "Заявки",
            "url": reverse("orders"),
            "icon_class": "bi-clipboard-data",
        },
        {
            "name": "Список услуг",
            "url": reverse("services-list"),
            "icon_class": "bi-list-check",
        },
    ]

    return {"menu_items": menu, "menu_staff_items": staff_menu}
