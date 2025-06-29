# Тема Django ORM Ч2. Знакомство с моделями и миграции. Урок 55

## Модели Django ORM

Мы упростили систему таблиц, для практики, и будем работать с этим, через установленный вчера `shell plus`

```python
from django.db import models


class Master(models.Model):
    name = models.CharField()
    phone = models.CharField()

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField()
    phone = models.CharField()
    comment = models.CharField()
    master = models.ForeignKey("Master", on_delete=models.SET_NULL, null=True, related_name='orders')

    def __str__(self):
        return f'Имя: {self.name}, телефон: {self.phone}'
```

`poetry run python manage.py shell_plus --print-sql`

## Практика с моделями

### Операция чтения - получаем одну запись - `get`, `first`, `last`


- Получить первый элемент - `first_order = Order.objects.first()`
- Получить последний элемент - `last_order = Order.objects.last()`
- Получить имя клиента из первой записи - `first_order.name`
- Получить имя мастера который будет обслуживать первую заявку - `first_order.master.name`
- Получим запись методом `get` - `order = Order.objects.get(id=1)` или `order = Order.objects.get(pk=1)`
- Получить все записи по мастеру - `order = Order.objects.get(name="Леголас")`

### Операция чтения - получаем коллекцию записей - `all` и `filter`

- Получить все заявки - `orders = Order.objects.all()`
- QuerySet - это коллекция, поэтому можно использовать все методы Django ORM
- Получить из этой коллекции элемент по индексу - `orders[0]`
- Или же получить последний элемент - `orders.last()`
  

### Операция создания - `create` и `save`

Создать запись можно 2мя способами:
- Через метод `save` (заранее создать объект)
- Через метод `create`

```python
# Получим первого попавшегося мастера
master = Master.objects.first()

new_order = Order(
    name='Фродо',
    phone='+3333',
    comment='Завивка')
# Можно добавлять данные до сохранения
new_order.master = master

new_order.save()


# Создадим заявку через метод create
new_order = Order.objects.create(
    name='Пиппин',
    phone='+4444',
    comment='Стрижка',
    master=master)
```

### Операция обновления - `update`


Обновление записи можно сделать 2мя способами:

- Через метод `save` (заранее создать объект)
- Через метод `update`

```python
# Получим первого попавшегося мастера
master = Master.objects.first()
master.name
master.name = 'Гендальф'
master.save()

# Uppdate - работает только с QuerySet
Order.objects.filter(pk=1).update(name='Гендальф')


# Добудем и обновим первую запись установим на второго мастера
Order.objects.filter(pk=1).update(master=Master.objects.get(name='Гендальф'))
```


### Операция удаления - `delete`

Создадим мастера Голума и удалим его

```python
# Создадим мастера Голума
master = Master.objects.create(name='Голум', phone='+5555')
# Удалим мастера
master.delete()
```

### Выборки через `filter` и `lookup __`

```python
# Получить все заявки Гендальфа
Order.objects.filter(master__name='Гендальф')

# Если у нас есть имя обратной ссылки - related_name='orders' то можно это сделать из мастеров
gendalfs_orders = Master.objects.get(name='Гендальф').orders.all()
gendalfs_orders
```

## Создание модели `Service`

Посмотрим как будут работать связи многие ко многим. Создадим модель `Service` и дадим ссылки из мастеров и из заказов.

```python
from django.db import models


class Master(models.Model):
    name = models.CharField()
    phone = models.CharField()
    services = models.ManyToManyField("Service", related_name='masters')

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField()from django.db import models


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

## Практика с моделями ManyToMany

Создадим записи в таблицу `Service`

```python
# Создадим записи в таблицу Service
Service.objects.create(name='Стрижка бороды', price='1000')
Service.objects.create(name='Укладка усов', price='1500')
Service.objects.create(name='Окрашивание бороды', price='2000')
```

Подключим новую модель в `admin.py`
```python
from django.contrib import admin
from .models import Master, Order, Service
admin.site.register(Master)
admin.site.register(Order)
admin.site.register(Service)
```

## Создание связей ManyToMany

- `add` - добавить запись в связь
- `remove` - удалить запись из связи
- `clear` - удалить все записи из связи
- `set` - заменить все записи в связи
- `all` - получить все записи из связи

```python
# Найду заявку где имя Пиппин
order = Order.objects.get(name='Пиппин')
# Получим все услуги
services = order.services.all()

# Добудем все услуги из БД
all_services = Service.objects.all()

# Удалим у Пиппина услуги
order.services.clear()

# Добавить полный список услуг
order.services.set(all_services)