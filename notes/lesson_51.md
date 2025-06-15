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




#### 1. Настройка шаблонов (25 мин)
- **Ключевые технологии**:
  - `TEMPLATES.DIRS` - добавление пути к шаблонам
  ```python
  # settings.py
  TEMPLATES = [
      {
          'DIRS': [os.path.join(BASE_DIR, 'templates')],
      }
  ]
  ```
  - `os.path.join()` - кроссплатформенные пути
  - Структура папок шаблонов:
    - `templates/` (корень проекта)
    - `templates/core/` (для приложения)

#### 2. Маршрутизация (40 мин)
- **Основные методы**:
  - `path()` - параметры и синтаксис:
    ```python
    # urls.py
    path(
        'orders/<int:order_id>/',  # URL с параметром
        views.order_detail,         # view-функция
        name='order_detail'         # имя маршрута
    )
    ```
  - Конвертеры путей: `int`, `str`, `slug`
  - Именованные маршруты: `reverse('route_name')`

#### 3. Работа с представлениями (45 мин)
- **Технологии**:
  - `render()` - параметры и контекст:
    ```python
    return render(
        request,
        'core/order_detail.html',  # путь к шаблону
        {'order': order_data}       # контекст
    )
    ```
  - `HttpResponse` vs `render` - когда использовать
  - Формирование контекста:
    - Передача списков словарей
    - Фильтрация данных в представлении

#### ⏸ Перерыв (15 мин)

#### 4. Шаблонизация (50 мин)
- **Ключевые концепции**:
  - Наследование шаблонов:
    ```html
    <!-- base.html -->
    {% block content %}{% endblock %}

    <!-- child.html -->
    {% extends "base.html" %}
    {% block content %}...{% endblock %}
    ```
  - Шаблонные теги:
    - `{% for item in list %}...{% endfor %}`
    - `{% if condition %}...{% endif %}`
  - Фильтры: `{{ value|lower }}`, `{{ date|date:"d.m.Y" }}`

#### 5. Статические файлы (30 мин)
- **Настройка**:
  ```python
  # settings.py
  STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
  ```
- **Использование в шаблонах**:
  ```html
  {% load static %}
  <link href="{% static 'css/main.css' %}" rel="stylesheet">
  <script src="{% static 'js/main.js' %}"></script>
  ```

#### 6. Практические паттерны (25 мин)
- **Техники**:
  - Централизация настроек в `settings.py`
  - Организация контекста (словари vs объекты)
  - Обработка ошибок 404 для несуществующих объектов
  - Использование `{% url 'name' %}` в шаблонах

#### Ключевые инструменты для ДЗ:
1. `path()` - маршрутизация
2. `render()` - рендеринг шаблонов
3. `{% extends %}`/`{% block %}` - наследование шаблонов
4. `{% static %}` - работа со статикой
5. `os.path.join()` - работа с путями
