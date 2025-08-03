# core/views.py
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib import messages
from .models import Order, Master, Service, Review
from .forms import ServiceForm, OrderForm, ReviewModelForm
from django.db.models import Q, Count, Sum, F

# Импорт классовых вью, View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse_lazy, reverse


class AjaxMasterServicesView(View):
    """
    Вью для отдачи массива объектов услуг по ID мастера.
    Обслуживает AJAX запросы формы создания заказа.
    """

    def get(self, request, master_id):
        master = Master.objects.prefetch_related("services").get(id=master_id)
        services = master.services.all()

        services_data = [
            {"id": service.id, "name": service.name} for service in services
        ]

        return JsonResponse({"services": services_data})


def review_create(request):
    if request.method == "GET":
        form = ReviewModelForm()
        return render(request, "review_class_form.html", {"form": form})

    elif request.method == "POST":
        form = ReviewModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Перенаправим на thanks и передадим source = review-create
            return redirect("thanks", source="review-create")
        else:
            return render(request, "review_class_form.html", {"form": form})

class LandingTemplateView(TemplateView):
    """Классовая view для главной страницы"""

    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["masters"] = Master.objects.prefetch_related("services").annotate(
            num_services=Count("services")
        )
        context["services"] = Service.objects.all()
        context["reviews"] = Review.objects.all()

        return context


class ThanksTemplateView(TemplateView):
    """
    Классовая view для маршрута 'thanks/'
    """

    template_name = "thanks.html"

    def get_context_data(self, **kwargs):
        """
        Расширение get_context_data для возможности передать в шаблон {{ title }} и {{ message }}.

        Они будут разные, в зависимости от куда пришел человек.
        Со страницы order/create/ с псевдонимом order-create
        Или со страницы review/create/ с псевдонимом review-create
        """
        context = super().get_context_data(**kwargs)

        if kwargs["source"]:
            source = kwargs["source"]
            if source == "order-create":
                context["title"] = "Спасибо за заказ!"
                context["message"] = (
                    "Ваш заказ принт. Скоро с вами свяжется наш менеджер для уточнения деталей."
                )
            elif source == "review-create":
                context["title"] = "Спасибо за отзыв!"
                context["message"] = (
                    "Ваш отзыв принят и отправлен на модерацию. После проверки он появится на сайте."
                )

        else:
            context["title"] = "Спасибо!"
            context["message"] = "Спасибо за ваше обращение!"

        return context


class OrderListView(ListView):
    model = Order
    template_name = "orders_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        queryset = super().get_queryset()
        # Получаю из GET запроса все данные URL
        # ПОИСКОВАЯ ФОРМА
        search_query = self.request.GET.get("q", "")
        # ЧЕКБОКСЫ выборки по полям
        # 1. поиск по телефону - search_by_phone
        # 2. поиск по имени - search_by_name
        # 3. поиск по тексту комментария - search_by_comment
        checkbox_name = self.request.GET.get("search_by_name", "")
        checkbox_phone = self.request.GET.get("search_by_phone", "")
        checkbox_comment = self.request.GET.get("search_by_comment", "")
        # ЧЕКББОКСЫ выборки по статусам
        # status_new
        # status_confirmed
        # status_completed
        # status_canceled
        checkbox_status_new = self.request.GET.get("status_new", "")
        checkbox_status_confirmed = self.request.GET.get("status_confirmed", "")
        checkbox_status_completed = self.request.GET.get("status_completed", "")
        checkbox_status_canceled = self.request.GET.get("status_canceled", "")

        # РАДИОКНОПКА Порядок сортировки по дате
        # order_by_date - desc, asc
        order_by_date = self.request.GET.get("order_by_date", "desc")

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
            queryset.prefetch_related("services")
            .select_related("master")
            .filter(search_q & status_q)
            .order_by(ordering)
        )

        return orders





class OrderDetailView(DetailView):
    model = Order
    template_name = "order_detail.html"
    context_object_name = "order"
    pk_url_kwarg = "order_id" # Указываем, что id брать из URL kwarg 'order_id'

    def get_queryset(self):
        """
        Лучшее место для "жадной" загрузки и аннотаций.
        Этот метод подготавливает оптимизированный QuerySet.
        """
        queryset = super().get_queryset()
        return queryset.select_related("master").prefetch_related("services").annotate(
            total_price=Sum("services__price")
        )

    def get_object(self, queryset=None):
        """
        Лучшее место для логики, специфичной для одного объекта.
        Например, для счетчика просмотров.
        """
        # Сначала получаем объект стандартным способом (он будет взят из queryset,
        # который мы определили в get_queryset)
        order = super().get_object(queryset)

        # Теперь выполняем логику с сессией и счетчиком
        session_key = f"order_{order.id}_viewed"
        if not self.request.session.get(session_key):
            self.request.session[session_key] = True
            # Атомарно увеличиваем счетчик в БД
            order.view_count = F("view_count") + 1
            order.save(update_fields=["view_count"])
            # Обновляем объект из БД, чтобы в шаблоне было актуальное значение
            order.refresh_from_db()

        return order

def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Заявка успешно отправлена!")
            return redirect("thanks", source="order-create")
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


class ServicesListView(ListView):
    model = Service
    # queryset = Service.objects.all().order_by("-price")
    template_name = "services_list.html"
    # object_list - стандартное имя для списка объектов
    # context_object_name = "services"


# def service_create(request):
#     if request.method == "GET":
#         # Создать пустую форму
#         form = ServiceForm()
#         context = {
#             "operation_type": "Создание услуги",
#             "form": form,
#         }
#         return render(request, "service_class_form.html", context=context)

#     elif request.method == "POST":
#         # Создаем форму и помещаем в нее данные из POST-запроса
#         form = ServiceForm(request.POST)

#         # Проверяем, что форма валидна
#         if form.is_valid():
#             # Создаем объект модели на основе данных из формы
#             form.save()
#             # Добавляем сообщение об успешном создании услуги
#             messages.success(request, "Услуга успешно создана!")
#             # Перенаправить на страницу со списком услуг
#             return redirect("services-list")
#         else:
#             messages.error(request, "Ошибка валидации формы! Проверьте введенные данные.")
#             context = {
#                 "operation_type": "Создание услуги",
#                 "form": form,
#             }
#             return render(request, "service_class_form.html", context=context)

#     else:
#         # Вернуть ошибку 405 (Метод не разрешен)
#         return HttpResponseNotAllowed(["GET", "POST"])


class ServiceCreateView(CreateView):
    form_class = ServiceForm
    template_name = "service_class_form.html"
    success_url = reverse_lazy("services-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = "Создание услуги"
        return context


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
