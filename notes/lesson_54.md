# Тема Django ORM Ч1. Знакомство с моделями и миграции. Урок 54

## Знакомство с концепцией миграций

- Что такое миграции
- Как миграции структурируют базу данных в соответствии с моделями
- Пример применения миграций для служебных таблиц

У нас всегда было сообщение про 18 непримененных миграций. Это миграции, которые создаются автоматически при создании проекта.
Эти приложения мы не видим, но они есть.

![django_standart_migrations_message.png](./images/django_standart_migrations_message.png)

## Применение служебных миграций

`poetry run python manage.py migrate` - команда для применения миграций

![standart_migrations.png](./images/standart_migrations.png)

В базе данных мы видим таблицы

![standart_tables_django.png](./images/standart_tables_django.png)

## Выполнение первой модели

Мы заходим в `./core/models.py` и создаем модель `Order`

```python
from django.db import models

class Order(models.Model):
    name = models.CharField()
    phone  = models.CharField()
    comment = models.CharField()
```

Теперь мы можем сделать миграцию и применить ее

```
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

![first_order_migrations.png](./images/first_order_migrations.png)

## Создание связи One-to-Many

```python
class Masetr(models.Model):
    name = models.CharField()
    phone = models.CharField()

class Order(models.Model):
    name = models.CharField()
    phone  = models.CharField()
    comment = models.CharField()
    master = models.ForeignKey("Master", on_delete=models.SET_NULL, null=True)

```

Установка Shell Plus 
`poetry add django-extensions`

Пдоключить в `settings.py`
```python
INSTALLED_APPS = [
    ...
    'django_extensions',
    'core',
```

Запускаем `poetry run python manage.py shell_plus`
Или же в режиме `print sql` - `poetry run python manage.py shell_plus --print-sql`