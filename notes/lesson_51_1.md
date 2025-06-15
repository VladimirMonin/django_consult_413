# Тема Django. MTV. Знакомство с Шаблонизатором и маршрутизацией. Урок 51

## Маршрутизация в Django: где находятся URLs и как работают конвертеры путей.

- Что такое конвертеры путей
- Синтаксис конвертеров `<>`
### Какие типы конвертеров существуют

- Сводная таблица с конвертерами, пример, что будет в переменной, когда рекомендуется использовать

- `orders` - Просто маршрут, без параметров
- `orders/<int:order_id>/` - Маршрут с параметром типа `int` с именем `order_id`
- `orders/<slug:order_slug>/` - Маршрут с параметром типа `slug` с именем `order_slug`
- `orders/<str:order_str>/` - Маршрут с параметром типа `str` с именем `order_str`
- `orders/<path:order_path>/` - Маршрут с параметром типа `path` с именем `order_path`
- `orders/<uuid:order_uuid>/` - Маршрут с параметром типа `uuid` с именем `order_uuid`

files/<path:file_path>/
files/anekdoty/GPT/obezianka/

file_path = "/anekdoty/GPT/obezianka/"

- Рассказ про каждый из типов маршрутов (заголовки 3 уровня)

## Создание маршрутов в нашем проекте

```python
from django.contrib import admin
from django.urls import path
from core.views import landing, thanks, orders_list, order_detail

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", landing),
    path("thanks/", thanks),
    path("orders/", orders_list),
    path("orders/<int:order_id>/", order_detail),
]
```
- Почему для главной страницы слеш не ставим
- Почему для остальных маршрутов обязательно ставим слеши
- Надо следить за тем чтобы маршруты были в едином стиле!

### Как работают параметры в путях?

- Что такое `order_id`
- Почему функция представление которая отвечает за этот маршрут должна принмать этот параметр?
- Какой тип данных может быть у этого параметра?

```python

def order_detail(request, order_id):
    """
    Отвечает за маршрут 'orders/<int:order_id>/'
    :param request: HttpRequest
    :param order_id: int (номер заказа)
    """
    return HttpResponse(f"<h1>Детали заказа {order_id}</h1>")
```

![order_detail_int_converter.png](./images/order_detail_int_converter.png)

- Рассказ о том как это работает под капотом в Django

### Модификация `order_detail`

Мы добавили датасет в `core/data.py` и теперь можем использовать его для поиска заказа по `order_id

Формат:

```python

orders = [
    {
        "id": 1,
        "client_name": "Пётр 'Безголовый' Головин",
        "services": ["Стрижка под 'Горшок'", "Полировка лысины до блеска"],
        "master_id": 1,
        "date": "2025-03-20",
        "status": STATUS_NEW,
    },
    ...
```

Функция которая у нас получилась

```python
from .data import orders

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
```

- Расскажи про функцию
- Расскажи про отдачу статус кодов
- Дай детальные пояснения что мы столкнулись с проблемой, где мы не можем давать гигантские HTML строки и что эту проблему решает шаблонизатор Django









