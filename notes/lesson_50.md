# Тема Django. MTV. Первые маршруты. Создание Django App. Урок 50

## Концепция приложений в Django

- Что такое
- Для чего надо
- Модульность

## Создание и подключение к проекту

- команда для создания
- как и где подключается

```bash
poetry run python manage.py startapp core
```

После чего нам нужно пройти в `barbershop/settings.py` и добавить наше приложение в `INSTALLED_APPS`

```python
# Пример
```

## Обзор созданного приложения `Core`

```txt
# Сделай ASCII схему с названиями файлов и кратким описанием
```

## Знакомство с MTV паттерном

![Схема описывающая паттерн MTV](./images/mtv_pattern.png)

- Описание паттерна
- Описане отличий от MVC

## Первый машрут

- Что такое path
- Что такое view
- Что такое HTTP Response
- Каждая вью обятаельно принемает request

```python
# core/views.py
from django.shortcuts import render, HttpResponse

def landing(request):
    return HttpResponse("<h1>Главная страница</h1>")

```

```python
# core/views.py
from django.shortcuts import render, HttpResponse

def landing(request):
    return HttpResponse("<h1>Главная страница</h1>")


```python
# barbershop/urls.py
from django.contrib import admin
from django.urls import path
from core.views import landing

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", landing),
]
```