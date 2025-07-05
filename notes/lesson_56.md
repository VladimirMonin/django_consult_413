# Тема Django ORM Ч3. Продвинутые выборки. Lookups. Урок 56

## Система таблиц

```python
from django.db import models


class Master(models.Model):
    name = models.CharField()
    phone = models.CharField()
    services = models.ManyToManyField("Service", related_name='masters')

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField()
    phone = models.CharField()
    comment = models.CharField()
    master = models.ForeignKey("Master", on_delete=models.SET_NULL, null=True, related_name='orders')
    services = models.ManyToManyField("Service", related_name='orders')

    def __str__(self):
        return f'Имя: {self.name}, телефон: {self.phone}'
    

class Service(models.Model):
    name = models.CharField()
    price = models.CharField()

    def __str__(self):
        return f'{self.name} - {self.price}'
```

## Что такое `Lookups`?

`Lookups` — это мощный инструмент в Django ORM, который позволяет выполнять сложные запросы к базе данных. Они позволяют фильтровать данные по определенным условиям, выполнять агрегационные функции и выполнять сложные выборки.

В первую очередь, это возможность сделать выборку с фильтрацией по связанным `m2m` и `o2m` полям.

# TODO - Дополнить конспект без использования лукапов типа gt gte - т.е. только для связанных данных

## Примеры работы с `Lookups` для связанных данных

### Выборка по связанным полям `o2m`

Выберем все заказы где мастер Гендальф

```python
# Получить все заявки, где имя мастера - 'Гендальф'
gendalfs_orders = Order.objects.filter(master__name='Гендальф')

# Это можно было бы сделать и через related_name
gendalfs_orders = Master.objects.get(name='Гендальф').orders.all()
```

# TODO - Дополнить дополнительной теорией

### Выборка по связанным полям `m2m`

Выбрать всех мастеров которые предоставляют услугу "Накручивание усов"

```python
# Получить всех мастеров, которые предоставляют услугу 'Накручивание усов'
masters_with_service = Master.objects.filter(services__name='Накручивание усов')
```

# TODO - Дополнить дополнительной теорией

## Lookups для более сложных запросов

`Lookups` также позволяют выполнять более сложные запросы, такие как:

- Больше, меньше, равно, не равно
- Выборка по диапазону
- Выборка по списку значений
- Выборка по подстроке
- Выборка по дате
- Выборка по регулярному выражению
- Выборка по `IN` и `NOT IN`
- Выборка по `ISNULL` и `NOT NULL`

# TODO - Расписать позиции детально текстом без кода

### Большая сводная таблица Lookups

Конечно, приношу извинения за краткость. Вот максимально полная сводная таблица лукапов Django ORM, включающая как самые популярные, так и более специфичные операторы для дат, времени и сложных полей.

Для примеров с датами и JSON предположим, что наши модели выглядят так:

```python
# models.py
from django.db import models
from datetime import date

# ... (существующие модели Master, Service)

class Order(models.Model):
    # ... (существующие поля)
    created_at = models.DateTimeField(auto_now_add=True) # Добавили поле с датой
    extra_data = models.JSONField(default=dict) # Добавили поле JSON
```

-----

### **Полная сводная таблица Django Lookups**

| Название (синтаксис) | Описание | Пример использования (на ваших моделях) | Доп. комментарии |
| :--- | :--- | :--- | :--- |
| **Основные и текстовые** |
| `field__exact` | Точное совпадение. | `Service.objects.filter(price__exact='1500')` | Используется по умолчанию, если лукап не указан. `filter(price='1500')` |
| `field__iexact` | Точное совпадение без учета регистра. | `Master.objects.filter(name__iexact='гендальф')` | `i` = insensitive. Полезно для логинов, имен. |
| `field__contains` | Содержит подстроку (с учетом регистра). | `Order.objects.filter(comment__contains='опозданием')` | Ищет вхождение в любом месте. |
| `field__icontains` | Содержит подстроку (без учета регистра). | `Order.objects.filter(comment__icontains='ОПОЗДАНИЕМ')` | **Один из самых используемых лукапов для поиска.** |
| `field__in` | Значение поля находится в списке. | `Order.objects.filter(name__in=['Срочный', 'VIP Заказ'])` | Очень эффективен для выборки по нескольким значениям. |
| `field__startswith` | Начинается с подстроки (с учетом регистра). | `Master.objects.filter(phone__startswith='8-800')` | Идеально для артикулов, префиксов. |
| `field__istartswith` | Начинается с подстроки (без учета регистра). | `Master.objects.filter(name__istartswith='ген')` | `i` = insensitive. |
| `field__endswith` | Заканчивается подстрокой (с учетом регистра). | `Order.objects.filter(phone__endswith='-99')` | Полезно для поиска по суффиксам. |
| `field__iendswith` | Заканчивается подстрокой (без учета регистра). | `Service.objects.filter(name__iendswith='УСОВ')` | `i` = insensitive. |
| **Числа и диапазоны** |
| `field__gt` | Больше чем (`>`). | `Service.objects.filter(price__gt='1000')` | `gt` = Greater Than. |
| `field__gte` | Больше или равно (`>=`). | `Service.objects.filter(price__gte='1000')` | `gte` = Greater Than or Equal. |
| `field__lt` | Меньше чем (`<`). | `Service.objects.filter(price__lt='500')` | `lt` = Less Than. |
| `field__lte` | Меньше или равно (`<=`). | `Service.objects.filter(price__lte='500')` | `lte` = Less Than or Equal. |
| `field__range` | Значение в диапазоне (включительно). | `Service.objects.filter(price__range=('500', '1500'))` | Принимает кортеж (tuple) из двух элементов. |
| **Даты и время** |
| `field__date` | Точное совпадение по дате (без времени). | `Order.objects.filter(created_at__date=date(2025, 7, 5))` | Сравнивает только `YYYY-MM-DD`. |
| `field__year` | Извлекает и сравнивает год. | `Order.objects.filter(created_at__year=2025)` | |
| `field__month` | Извлекает и сравнивает месяц (1-12). | `Order.objects.filter(created_at__month=7)` | |
| `field__day` | Извлекает и сравнивает день (1-31). | `Order.objects.filter(created_at__day=5)` | |
| `field__week` | Извлекает и сравнивает номер недели (1-53). | `Order.objects.filter(created_at__week=27)` | |
| `field__week_day` | Извлекает и сравнивает день недели (1=Вс, 2=Пн ... 7=Сб). | `Order.objects.filter(created_at__week_day=7)` | Найти все заказы, сделанные в субботу. |
| `field__quarter` | Извлекает и сравнивает квартал (1-4). | `Order.objects.filter(created_at__quarter=3)` | |
| `field__time` | Точное совпадение по времени (без даты). | `Order.objects.filter(created_at__time=time(15, 43))` | |
| `field__hour` | Извлекает и сравнивает час (0-23). | `Order.objects.filter(created_at__hour__gte=12)` | Найти все заказы, сделанные после полудня. |
| `field__minute` | Извлекает и сравнивает минуту (0-59). | `Order.objects.filter(created_at__minute=30)` | |
| `field__second` | Извлекает и сравнивает секунду (0-59). | `Order.objects.filter(created_at__second__lt=10)` | |
| **Отношения и `NULL`** |
| `field__isnull` | Проверяет, является ли значение `NULL`. | `Order.objects.filter(master__isnull=True)` | Принимает `True` или `False`. Найти заказы без мастера. |
| **Сложные типы и RegExp** |
| `field__regex` | Совпадает с RegExp (с учетом регистра). | `Master.objects.filter(name__regex=r'^(Г|С)\w+')` | Для очень сложных поисковых паттернов. |
| `field__iregex` | Совпадает с RegExp (без учета регистра). | `Master.objects.filter(name__iregex=r'^(г|с)\w+')` | `i` = insensitive. |
| `field__has_key` | `JSONField`: содержит ключ верхнего уровня. | `Order.objects.filter(extra_data__has_key='is_vip')` | Требуется `JSONField` и СУБД с поддержкой JSON (например, PostgreSQL). |
| `field__contains` | `JSONField`: JSON содержит переданный JSON. | `Order.objects.filter(extra_data__contains={'source': 'web'})` | Проверяет, что один JSON является подмножеством другого. |
| **Инвертирование** |
| `.exclude()` | **Не лукап, а метод QuerySet.** Инвертирует фильтр. | `Master.objects.exclude(name__startswith='А')` | Найти всех мастеров, чье имя НЕ начинается на 'А'. **Любой лукап можно инвертировать, поместив его в `.exclude()` вместо `.filter()`**. |
