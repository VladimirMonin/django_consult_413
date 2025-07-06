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

---

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

### Примеы запросов с использованием `Lookups`

```python
# Запустим shell plus в print-режиме
poetry run python manage.py shell_plus --print-sql

# Выбрать заказы где не указан мастер
Order.objects.filter(master__isnull=True)

# Все мастера где имя начинается на "Гендальф"
Master.objects.filter(name__startswith='Гендальф')

# Услуги дороже > 500 рублей
Service.objects.filter(price__gt='500')

# Заказы где мастер указан и начинается на "Г"
Order.objects.filter(master__isnull=False, master__name__startswith='Г')

# Можно использовать передачу аргументов через запятую, но можно и так
Order.objects.filter(master__isnull=False).filter(master__name__startswith='Г')

# Двойной лукап для связанного поля + для выборки по условию
```

### Практика

1. Выбрать все заказы где имя мастера входит в список: Гендальф, Фродо, Пиппин
`Order.objects.filter(master__name__in=['Гендальф', 'Фродо', 'Пиппин'])`
2. Выбрать все услуги в диапазоне цен от 500 до 1000 рублей
`Service.objects.filter(price__range=('500', '1000'))`
3. Выбрать все услуги где в название входит "ус" и цена больше 500 рублей
`Service.objects.filter(name__contains='ус', price__gt='500')`
4. Выбрать все заказы где услуга входит в список: "Стрижка", "Укладка", "Окрашивание"
`Order.objects.filter(service__name__in=['Стрижка', 'Укладка', 'Окрашивание'])`

# TODO - Описать понятным языком как формируются эти запросы и рассказать про решения практического задания. Разделить на 2 части: описание заданий и решение

### Работа с датой и временем

#### Типы принимаемых данных

Лукапы для даты и времени можно разделить на две группы по типу данных, которые они принимают:

1. **Принимают целые числа (`int`):** Эти лукапы извлекают из даты/времени одну конкретную часть (год, месяц, час и т.д.) и сравнивают её с переданным вами числом.

      - `year`, `month`, `day`, `week`, `week_day`, `quarter`, `hour`, `minute`, `second`

2. **Принимают объекты `date`, `time`, `datetime`:** Эти лукапы сравнивают значение поля в базе данных с полноценным объектом даты или времени из Python.

      - `date`, `time`, а также стандартные операторы сравнения (`gt`, `lt`, `gte`, `lte`, `range`) при работе с полями даты/времени.

-----

#### Детальная таблица лукапов

Предположим, у нас есть модель `Order` с полем `created_at = models.DateTimeField()`.

| Lookup | Что принимает | Описание и пример |
| :--- | :--- | :--- |
| **Лукапы, принимающие `int`** |
| `__year` | `int` | Фильтрует по году. `Order.objects.filter(created_at__year=2024)` |
| `__month` | `int` | Фильтрует по номеру месяца (1-12). `Order.objects.filter(created_at__month=7)` |
| `__day` | `int` | Фильтрует по дню месяца (1-31). `Order.objects.filter(created_at__day=5)` |
| `__week` | `int` | Фильтрует по номеру недели в году (1-53). `Order.objects.filter(created_at__week=27)` |
| `__week_day`| `int` | Фильтрует по дню недели (1=Вс, **2=Пн** ... 7=Сб). `Order.objects.filter(created_at__week_day=2)` (все заказы за понедельник) |
| `__quarter`| `int` | Фильтрует по кварталу года (1-4). `Order.objects.filter(created_at__quarter=3)` (заказы 3-го квартала) |
| `__hour` | `int` | Фильтрует по часу (0-23). `Order.objects.filter(created_at__hour=15)` (заказы, сделанные в 15:xx) |
| `__minute` | `int` | Фильтрует по минуте (0-59). `Order.objects.filter(created_at__minute__gte=30)` (заказы, сделанные во второй половине часа) |
| `__second` | `int` | Фильтрует по секунде (0-59). `Order.objects.filter(created_at__second=0)` |
| **Лукапы, принимающие объекты** |
| `__date` | `date` объект | Сравнивает только дату, игнорируя время. `from datetime import date`\<br\>`Order.objects.filter(created_at__date=date(2025, 7, 5))` |
| `__time` | `time` объект | Сравнивает только время, игнорируя дату. `from datetime import time`\<br\>`Order.objects.filter(created_at__time__gt=time(18, 0))` |

-----

### Как с этим работать: Практические примеры

Для этих примеров импортируем необходимые модули:
`from datetime import datetime, date, time, timedelta`

#### Выборка "позже" и "раньше"

Для сравнения используются стандартные лукапы `gt` (позже), `lt` (раньше), `gte` (позже или равно), `lte` (раньше или равно), которым передается **полноценный `datetime` объект**.

- **Найти все заказы, созданные *после* определенного момента:**

```python
specific_moment = datetime(2025, 7, 5, 12, 0, 0)
late_orders = Order.objects.filter(created_at__gt=specific_moment)
```

- **Найти все заказы, созданные за последние 24 часа:**

```python
time_threshold = datetime.now() - timedelta(hours=24)
recent_orders = Order.objects.filter(created_at__gte=time_threshold)
```

#### Вхождение в диапазон

Используется лукап `__range`, который принимает кортеж (tuple) из двух `datetime` объектов: начало и конец диапазона.

- **Найти все заказы, сделанные в рабочие часы (с 9 до 18) в конкретный день:**

```python
start_time = datetime(2025, 7, 5, 9, 0)
end_time = datetime(2025, 7, 5, 18, 0)
work_hour_orders = Order.objects.filter(created_at__range=(start_time, end_time))
```

#### Комбинирование лукапов

Вы можете объединять разные лукапы для создания точных запросов.

- **Найти все заказы за Июль, сделанные в первой половине дня (до 12:00):**

```python
july_morning_orders = Order.objects.filter(
    created_at__month=7,
    created_at__hour__lt=12
)
```

- **Найти все заказы, сделанные в выходные (суббота и воскресенье) в 2024 году:**

```python
from django.db.models import Q

weekend_orders_2024 = Order.objects.filter(
    created_at__year=2024,
    created_at__week_day__in=[1, 7] # 1=Воскресенье, 7=Суббота
)
# Альтернатива с Q-объектом
weekend_orders_2024_alt = Order.objects.filter(
    created_at__year=2024,
    Q(created_at__week_day=1) | Q(created_at__week_day=7)
)
```

## Q Объект как решение для сложных запросов с использованием логических операторов

### Q объект - определение

`Q` объект в Django ORM используется для создания сложных запросов, которые включают логические операторы (`AND`, `OR`, `NOT`). Он позволяет объединять различные условия в один запрос, чтобы получить более точные результаты.

### Использование Q объекта

```python
from django.db.models import Q

# Разные варианты использования Q объекта

# 1. Создать заранее
q_object = Q(name='John')

order_query = Order.objects.filter(q_object)

# 2. Использовать Q создавая его прямо внутри фильтра
order_query = Order.objects.filter(
    Q(name='Пиппин') | Q(name='Фродо')
)

# ОПЕРАТОРЫ: | - OR, & - AND, ~ - NOT
# ИНПЛЕЙС ОПЕРАТОРЫ |=, &=, ~=


# 3. Использовать Q "накапливая условия" через инплейс операторы

# Пустой объфект
q_object = Q()

# Добавляем условие
q_object &= Q(name='Пиппин')

# Добавляем второе условие
q_object &= Q(name='Фродо')

# Сделать запрос
order_query = Order.objects.filter(q_object)
```

### Примеры использования Q объекта

#### Пример 1: Фильтрация заказов по имени (OR точное совпадение)

```python
from django.db.models import Q
filtered_orders = Order.objects.filter(
    Q(name='Пиппин') | Q(name='Фродо')
)
```

#### Пример 2: Фильтрация заказов по имени (OR имя начинается на "Гендальф" или "Саурон")

```python
filtered_orders = Order.objects.filter(
    Q(name__startswith='Гендальф') | Q(name__startswith='Саурон')
)
```

#### Пример 3: Фильтрация мастеров которые оказывают 2 услуги (AND)

```python
filtered_masters = Master.objects.filter(
    Q(services__name='Тараканьи усы') & Q(services__name='Гном борода')
)
```

#### Пример 4: Фильтрация мастеров которые оказывают (УСЛУГА или УСЛУГА) И (УСЛУГА или УСЛУГА)

```python
filtered_masters = Master.objects.filter(
    (Q(services__name='Тараканьи усы') | Q(services__name='Спиральные усы')) & (Q(services__name='Гном борода') | Q(services__name='Тролль стайл'))
)
```

#### Пример 5: Фильтрация мастеров которые оказывают УСЛУГА или УСЛУГА И УСЛУГА или УСЛУГА

```python
filtered_masters = Master.objects.filter(
    Q(services__name='Тараканьи усы') | Q(services__name='Спиральные усы') & Q(services__name='Гном борода') | Q(services__name='Тролль стайл')
)
```
Разница между 4 и 5 запросом будет огромна. Хотя визуально ни отличаются только скобками - это приоритеты выполнения запроса.

Приоритеты такие же как и в пайтон и sql

- () - самый высокий приоритет №1 - логическая группировка
- `~` - приоритет №2 - логическое отрицание
- `&` - приоритет №3 - логическое И
- `|` - приоритет №4 - логическое ИЛИ

Скриншот который визуально отображает приоритеты
![q_priority.png](./images/q_priority.png)

### Практика с Q объектом

1. Найти услуги где в название входит "усы" или "борода" 
2. Дописать запрос 1 - добавить И цена ниже 1000
3. Дописать запрос 2 - добавить общее на выражение ИЛИ в название входит стрижка и цена ниже 500