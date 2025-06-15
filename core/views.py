# core/views.py
from django.shortcuts import render, HttpResponse


def landing(request):
    """
    Отвечает за маршрут '/'
    """
    return HttpResponse("<h1>Главная страница</h1>")


def thanks(request):
    """
    Отвечает за маршрут 'thanks/'
    """
    return HttpResponse("<h1>Спасибо за заказ!</h1>")


def orders_list(request):
    """
    Отвечает за маршрут 'orders/'
    """
    return HttpResponse("<h1>Список заказов</h1>")


def order_detail(request, order_id):
    """
    Отвечает за маршрут 'orders/<int:order_id>/'
    :param request: HttpRequest
    :param order_id: int (номер заказа)
    """
    return HttpResponse(f"<h1>Детали заказа {order_id}</h1>")

