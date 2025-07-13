# Тема Django ORM Ч5. Annotate, prefetch, F-object, DDT. Урок 58

## Prefetch - как способ избежать N+1

Описание проблемы:

- Ленивый Django ORM
- Нет подгрузки связанных данных m2m o2m
- Когда шаблонизатор работает - создается много запросов
- Особенно чувствительно для m2m
- Пример с блогом (пост, категория, теги)

******

## Debug Toolbar

![django_orm_prefetch_example.png](./images/django_orm_prefetch_example.png)

Документация: <https://django-debug-toolbar.readthedocs.io/en/latest/installation.html>

`poetry add django-debug-toolbar`

```python
# settings.py
INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS += [
   'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
```

```python
# urls.py
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    # ... the rest of your URLconf goes here ...
] + debug_toolbar_urls()
```

******

## Два метода: prefetch_related и select_related

Первый `prefetch_related` - позволяет загрузить связанные данные, оптимирован для типа m2m
Второй `select_related` - оптимизирован для связей 1-1 и 1-n

select_related: Используется для связей "один-к-одному" (OneToOneField) и "один-ко-многим" (ForeignKey). Он работает, создавая SQL JOIN и извлекая данные из связанных таблиц в одном и том же запросе к базе данных. Это очень эффективно, так как позволяет избежать дополнительных запросов.

prefetch_related: Используется для связей "многие-ко-многим" (ManyToManyField) и обратных связей "один-ко-многим". Он работает иначе: сначала выполняется основной запрос, а затем для каждой связи выполняется отдельный запрос. После этого Django "соединяет" данные уже в Python. Этот метод решает проблему N+1 для связей, где JOIN был бы неэффективен или невозможен.

******

## Объект Prefetch

Объект `Prefetch` используется тогда, когда вам нужна **большая гибкость** при предварительной загрузке данных, чем может предложить простой вызов `prefetch_related('field_name')`.

Основные сценарии, когда стоит использовать объект `Prefetch`:

1. **Фильтрация связанных объектов**: Когда вы хотите загрузить не все связанные объекты, а только те, которые соответствуют определенным критериям.
2. **Дальнейшая оптимизация запроса к связанным объектам**: Когда вы хотите применить `select_related` или `annotate` к запросу, который извлекает связанные данные.
3. **Сохранение результата в новый атрибут**: Чтобы не перезаписывать стандартный менеджер связей (`master.services`), а сохранить отфильтрованный результат в отдельный атрибут (например, `master.popular_services`).

### Практический пример на ваших моделях

Давайте посмотрим на ваши модели в [`core/models.py`](core/models.py:1). У вас есть модель `Master` и `Service` со связью "многие-ко-многим". Услуги (`Service`) имеют флаг `is_popular`.

**Задача**: Получить список всех мастеров и для каждого из них предварительно загрузить **только популярные** услуги.

Если использовать `Master.objects.prefetch_related('services')`, Django загрузит *все* услуги для каждого мастера, и фильтровать их придется уже в коде Python, что неэффективно.

Вот как эту задачу решает `Prefetch`:

```python
from django.db.models import Prefetch
from core.models import Master, Service

# 1. Создаем queryset, который выбирает только популярные услуги.
popular_services_qs = Service.objects.filter(is_popular=True)

# 2. Используем Prefetch, чтобы указать Django, как именно загружать данные.
#    - 'services': поле для предзагрузки.
#    - queryset: наш специальный queryset для фильтрации.
#    - to_attr: имя нового атрибута для хранения результата.
masters = Master.objects.prefetch_related(
    Prefetch('services', queryset=popular_services_qs, to_attr='popular_services')
)

# 3. Теперь мы можем эффективно использовать эти данные.
for master in masters:
    print(f"Мастер: {master.name}")
    # Атрибут 'popular_services' содержит только отфильтрованные данные
    # и не требует дополнительных запросов к БД.
    for service in master.popular_services:
        print(f"  -> Популярная услуга: {service.name}")
```

В этом примере мы выполнили всего два запроса к базе данных:

1. Один для получения всех мастеров.
2. Второй для получения всех популярных услуг, связанных с этими мастерами.

Затем Django соединил эти данные в Python. Это гораздо эффективнее, чем выполнять отдельный запрос для каждого мастера.

Я добавил это подробное объяснение с примером в ваш файл с заметками [`notes/lesson_58.md`](notes/lesson_58.md).

******

## Annotate

`annotate` - это метод, который позволяет добавлять вычисляемые атрибуты к запросу. Это может быть полезно, когда вы хотите выполнить агрегацию данных, например, подсчитать количество связанных объектов или выполнить математические операции.

Это старые добрые агрегатные функции из SQL которые мы изучали

- MIN
- MAX
- AVG
- SUM
- COUNT

```python
from django.db.models import Count

# Посчитаем количество услуг для каждого мастера
masters = Master.objects.annotate(num_services=Count('services')).all()
```

Тут мы группируем по мастерам и считаем количество связанных услуг для каждого мастера.
Ложим результат в атрибут `num_services`

******

### Использование `annotate` с `prefetch_related`

```python
from django.db.models import Prefetch, Count
masters = Master.objects.prefetch_related('services').annotate(num_services=Count('services'))
```

Запуск Shell Plus print-sql

```bash
poetry run python manage.py shell_plus --print-sql
```
