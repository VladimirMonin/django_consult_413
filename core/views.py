# core/views.py
from django.shortcuts import render, HttpResponse
from .data import orders
from .models import Order, Master, Service
from django.contrib.auth.decorators import login_required


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
    orders = Order.objects.all()
    context = {
        "orders": orders,
    }
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
