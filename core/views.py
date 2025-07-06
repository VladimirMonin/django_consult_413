# core/views.py
from django.shortcuts import render, HttpResponse
from .data import orders
from .models import Order, Master, Service
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def landing(request):
    """
    Отвечает за маршрут '/'
    """
    return HttpResponse("<h1>Главная страница</h1>")


def thanks(request):
    """
    Отвечает за маршрут 'thanks/'
    """
    context = {"test_var": "Привет из базового шаблона!"}
    return render(request, "thanks.html", context=context)


@login_required
def orders_list(request):
    """
    Отвечает за маршрут 'orders/'
    """
    # Получаю из GET запроса все данные URL
    # ПОИСКОВАЯ ФОРМА
    search_query = request.GET.get("q", "")
    # ЧЕКБОКСЫ выборки по полям
    # 1. поиск по телефону - search_by_phone
    # 2. поиск по имени - search_by_name
    # 3. поиск по тексту комментария - search_by_comment
    checkbox_name = request.GET.get("search_by_name", "")
    checkbox_phone = request.GET.get("search_by_phone", "")
    checkbox_comment = request.GET.get("search_by_comment", "")
    # ЧЕКББОКСЫ выборки по статусам
    # status_new
    # status_confirmed
    # status_completed
    # status_canceled
    checkbox_status_new = request.GET.get("status_new", "")
    checkbox_status_confirmed = request.GET.get("status_confirmed", "")
    checkbox_status_completed = request.GET.get("status_completed", "")
    checkbox_status_canceled = request.GET.get("status_canceled", "")

    # РАДИОКНОПКА Порядок сортировки по дате
    # order_by_date - desc, asc
    order_by_date = request.GET.get("order_by_date", "desc")

    # Формируем Q пустой
    q = Q()

    # Если есть поиск по телефону
    if checkbox_phone:
        # Добавляем в Q условие поиска по телефону
        q |= Q(phone__icontains=search_query)
    # Если есть поиск по имени
    if checkbox_name:
        # Добавляем в Q условие поиска по имени
        q |= Q(name__icontains=search_query)
    if checkbox_comment:
        # Добавляем в Q условие поиска по комментарию
        q |= Q(comment__icontains=search_query)

    # Группа по статусам
    # Если есть статус "Новый"
    if checkbox_status_new:
        # Добавляем в Q условие поиска по статусу "Новый"
        q |= Q(status="new")
    # Если есть статус "Подтвержден"
    if checkbox_status_confirmed:
        # Добавляем в Q условие поиска по статусу "Подтвержден"
        q |= Q(status="confirmed")
    # Если есть статус "Выполнен"
    if checkbox_status_completed:
        # Добавляем в Q условие по иска по статусу "Выполнен"
        q |= Q(status="completed")
    if checkbox_status_canceled:
        # Добавляем в Q условие по иска по статусу "Отменен"
        q |= Q(status="canceled")

    ordering = "-date_created" if order_by_date == "desc" else "date_created"
    orders = Order.objects.filter(q).order_by(ordering)

    context = {"orders": orders}

    return render(request, "orders_list.html", context=context)


@login_required
def order_detail(request, order_id):
    """
    Отвечает за маршрут 'orders/<int:order_id>/'
    :param request: HttpRequest
    :param order_id: int (номер заказа)
    """
    order = [order for order in orders if order["id"] == order_id]
    try:
        order = order[0]
        context = {
            "order": order,
            "my_fariable": "Hello, world!",
        }
    except IndexError:
        return HttpResponse("<h1>Заказ не найден</h1>", status=404)

    else:
        return render(request, "order_detail.html", context=context)
