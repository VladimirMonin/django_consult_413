# core/views.py
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib import messages
from .data import orders
from .models import Order, Master, Service
from .forms import OrderForm
from django.db.models import Q, Count, Sum



def landing(request):
    """
    Отвечает за маршрут '/'
    """
    # masters = Master.objects.prefetch_related("services").all()
    masters = Master.objects.prefetch_related('services').annotate(num_services=Count('services'))
    
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
    orders = Order.objects.prefetch_related("services").select_related("master").filter(search_q & status_q).order_by(ordering)

    context = {"orders": orders}

    return render(request, "orders_list.html", context=context)


def order_detail(request, order_id):
    """
    Отвечает за маршрут 'orders/<int:order_id>/'
    :param request: HttpRequest
    :param order_id: int (номер заказа)
    """
    order = Order.objects.prefetch_related("services").select_related("master").annotate(total_price=Sum('services__price')).get(id=order_id)

    #TODO Добавить в модель Order view_count. Миграции. Дописать логику обновления через F объект. Сделать коммит. Допишу логику с сохранением в сессию во избежании накруторк!

    context = {"order": order}

    return render(request, "order_detail.html", context=context)


def order_page(request):
    form = OrderForm()
    return render(request, 'order_page.html', {'form': form})

def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Заявка успешно отправлена!")
            return redirect("thanks")
        # Если форма невалидна, снова рендерим страницу с формой и ошибками
        return render(request, 'order_page.html', {'form': form})
    # Если метод не POST, перенаправляем на страницу с формой
    return redirect('order-page')


def services_list(request):
    services = Service.objects.all()
    return render(request, "services_list.html", {"services": services})



def service_create(request):
    if request.method == "GET":
        # Дать пустой шаблон
        context = {
            "operation_type": "Создание услуги",
        }
        return render(request, "service_form.html", context=context)
    
    elif request.method == "POST":
        # Получить данные из объекта запроса
        service_name = request.POST.get("service_name")
        service_description = request.POST.get("service_description")
        service_price = request.POST.get("service_price")

        if service_name and service_description and service_price and service_price.isdigit():
            # Создать объект сервиса
            service = Service.objects.create(
                name=service_name,
                description=service_description,
                price=service_price
            )
            
            # Перенаправить на страницу со списком услуг
            return redirect("services-list")
        else:
            messages.error(request, "Ошибка при создании услуги")

            context = {
                "operation_type": "Создание услуги",
            }
            return render(request, "service_form.html", context=context)
        
    else:
        # Вернуть ошибку 405 (Метод не разрешен)
        return HttpResponseNotAllowed(["GET", "POST"])


def service_update(request, service_id):
    if request.method == "GET":
        # Дать форму с данными этой услуги
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            # Если нет такой услуги, дам 404
            return HttpResponse("Услуга не найдена", status=404)
        
        
        
        context = {
            "operation_type": "Обновление услуги",
            "service": service,

        }
        return render(request, "service_form.html", context=context)
    
    elif request.method == "POST":
        # Получить данные из объекта запроса
        service_name = request.POST.get("service_name")
        service_description = request.POST.get("service_description")
        service_price = request.POST.get("service_price")

        

        # Получить объект сервиса
        service = Service.objects.get(id=service_id)
        service_price = float(service_price.replace(",", "."))
        if service_name and service_description and service_price:
            
            # Создать объект сервиса
            service = Service.objects.update(
                name=service_name,
                description=service_description,
                price=service_price
            )

            
    
            # Перенаправить на страницу со списком услуг
            return redirect("services-list")
        else:
            messages.error(request, "Ошибка при создании услуги")

            context = {
                "operation_type": "Обновление услуги",
                "service": service,
            }
            return render(request, "service_form.html", context=context)
        
    else:
        # Вернуть ошибку 405 (Метод не разрешен)
        return HttpResponseNotAllowed(["GET", "POST"])