# core/context_processors.py
from django.urls import reverse


def menu_items(request):
    """
    Контекстный процессор для добавления меню в контекст шаблонов.
    """
    menu = [
        {"title": "Главная", "url_name": "main", "url": reverse("main")},
        {
            "title": "Мастера",
            "url": reverse("main") + "#masters",
        },
        {
            "title": "Услуги",
            "url": reverse("main") + "#services",
        },
        {
            "title": "Отзывы",
            "url": reverse("main") + "#reviews",
        },
        {
            "title": "Записаться",
            "url": reverse("main") + "#get-order",
        },
    ]

    menu_staff = [
        {"title": "Заявки", "url": reverse("orders")},
    ]

    return {"menu_items": menu, "menu_staff_items": menu_staff}
