# core/views.py
from django.shortcuts import render, HttpResponse
from .data import orders


def landing(request):
    """
    Отвечает за маршрут '/'
    """
    return HttpResponse("<h1>Главная страница</h1>")


def thanks(request):
    """
    Отвечает за маршрут 'thanks/'
    """
    return render(request, "thanks.html")


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
    order = [order for order in orders if order["id"] == order_id]
    try:
        order = order[0]
    
    except IndexError:
        return HttpResponse("<h1>Заказ не найден</h1>", status=404)
    
    else:
        order_data = f"""<h1>Заказ {order["id"]}</h1><p>Клиент: {order["client_name"]}</p>"""
        return HttpResponse(order_data)
