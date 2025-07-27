# core/views.py
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib import messages
from .data import orders
from .models import Order, Master, Service, Review
from .forms import ServiceForm, OrderForm, ReviewModelForm
from django.db.models import Q, Count, Sum


def get_services_by_master(request, master_id):
    master = Master.objects.prefetch_related("services").get(id=master_id)
    services = master.services.all()

    services_data = [{"id": service.id, "name": service.name} for service in services]

    return JsonResponse({"services": services_data})

def review_create(request):
    if request.method == "GET":
        form = ReviewModelForm()
        return render(request, "review_class_form.html", {"form": form})
    
    elif request.method == "POST":
        form = ReviewModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("landing")
        else:
            return render(request, "review_class_form.html", {"form": form})




def landing(request):
    """
    Отвечает за маршрут '/'
    """
    # masters = Master.objects.prefetch_related("services").all()
    masters = Master.objects.prefetch_related("services").annotate(
        num_services=Count("services")
    )

    # Получаем все услуги отдельным запросом
    services = Service.objects.all()

    # reviews = Review.objects.all()  # Модель Review еще не создана

    context = {
        "masters": masters,
        "services": services,
        # "reviews": reviews,
    }
    return render(request, "landing.html", context=context)


def thanks(request):
    """
    Отвечает за маршрут 'thanks/'
    """
    context = {"test_var": "Привет из базового шаблона!"}
    return render(request, "thanks.html", context=context)


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

    # 1. Создаем Q-объект для текстового поиска
    search_q = Q()
    if search_query:
        # Внутренние условия поиска объединяем через ИЛИ (|=)
        if checkbox_phone:
            search_q |= Q(phone__icontains=search_query)
        if checkbox_name:
            search_q |= Q(name__icontains=search_query)
        if checkbox_comment:
            search_q |= Q(comment__icontains=search_query)

    # 2. Создаем Q-объект для фильтрации по статусам
    status_q = Q()
    # Условия статусов тоже объединяем через ИЛИ (|=)
    if checkbox_status_new:
        status_q |= Q(status="new")
    if checkbox_status_confirmed:
        status_q |= Q(status="confirmed")
    if checkbox_status_completed:
        status_q |= Q(status="completed")
    if checkbox_status_canceled:
        status_q |= Q(status="canceled")

    # Порядок сортировки
    ordering = "-date_created" if order_by_date == "desc" else "date_created"

    # 3. Объединяем два Q-объекта через И (&)
    # Это гарантирует, что запись должна соответствовать И условиям поиска, И условиям статуса
    orders = (
        Order.objects.prefetch_related("services")
        .select_related("master")
        .filter(search_q & status_q)
        .order_by(ordering)
    )

    context = {"orders": orders}

    return render(request, "orders_list.html", context=context)


def order_detail(request, order_id):
    """
    Отвечает за маршрут 'orders/<int:order_id>/'
    :param request: HttpRequest
    :param order_id: int (номер заказа)
    """
    order = (
        Order.objects.prefetch_related("services")
        .select_related("master")
        .annotate(total_price=Sum("services__price"))
        .get(id=order_id)
    )

    # TODO Добавить в модель Order view_count. Миграции. Дописать логику обновления через F объект. Сделать коммит. Допишу логику с сохранением в сессию во избежании накруторк!

    context = {"order": order}

    return render(request, "order_detail.html", context=context)


def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Заявка успешно отправлена!")
            return redirect("thanks")
    else:
        form = OrderForm()

    return render(request, "order_class_form.html", {"form": form})


def order_update(request, order_id):
    """
    Отвечает за маршрут 'orders/<int:order_id>/update/'
    """
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponse("Заказ не найден", status=404)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f"Заказ №{order.id} успешно обновлен.")
            return redirect("order_detail", order_id=order.id)
    else:
        form = OrderForm(instance=order)

    context = {
        "form": form,
        "operation_type": f"Обновление заказа №{order.id}",
    }
    return render(request, "order_class_form.html", context)


def services_list(request):
    services = Service.objects.all()
    return render(request, "services_list.html", {"services": services})


def service_create(request):
    if request.method == "GET":
        # Создать пустую форму
        form = ServiceForm()
        context = {
            "operation_type": "Создание услуги",
            "form": form,
        }
        return render(request, "service_class_form.html", context=context)

    elif request.method == "POST":
        # Создаем форму и помещаем в нее данные из POST-запроса
        form = ServiceForm(request.POST)

        # Проверяем, что форма валидна
        if form.is_valid():
            # Добываем данные из формы
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            duration = form.cleaned_data["duration"]
            is_popular = form.cleaned_data["is_popular"]
            image = form.cleaned_data["image"]

            # Создать объект услуги
            service = Service(
                name=name,
                description=description,
                price=price,
                duration=duration,
                is_popular=is_popular,
                image=image,
            )
            # Сохранить объект в БД
            service.save()

            # Перенаправить на страницу со списком услуг
            return redirect("services-list")
        else:
            context = {
                "operation_type": "Создание услуги",
                "form": form,
            }
            return render(request, "service_class_form.html", context=context)

    else:
        # Вернуть ошибку 405 (Метод не разрешен)
        return HttpResponseNotAllowed(["GET", "POST"])


def service_update(request, service_id):
    """
    Отвечает за маршрут 'services/<int:service_id>/update/'
    """
    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        # Если нет такой услуги, вернем 404
        return HttpResponse("Услуга не найдена", status=404)

    if request.method == "GET":
        # Для GET-запроса создаем форму, связанную с существующим объектом
        form = ServiceForm(instance=service)
        context = {
            "operation_type": "Обновление услуги",
            "form": form,
        }
        return render(request, "service_class_form.html", context=context)

    elif request.method == "POST":
        # Для POST-запроса создаем форму с данными из запроса и связываем с объектом
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            # Если форма валидна, сохраняем изменения
            form.save()
            messages.success(request, f"Услуга '{service.name}' успешно обновлена.")
            return redirect("services-list")
        else:
            # Если форма невалидна, снова отображаем страницу с формой и ошибками
            context = {
                "operation_type": "Обновление услуги",
                "form": form,
            }
            return render(request, "service_class_form.html", context=context)

    else:
        # Для всех других методов возвращаем ошибку
        return HttpResponseNotAllowed(["GET", "POST"])
