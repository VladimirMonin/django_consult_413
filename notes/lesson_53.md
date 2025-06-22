# Тема Django. Наследование шаблонов. Include. Контекстный процессор. Урок 53

## Что такое наследование шаблонов в Django? 🤔

# TODO Сделать из этих пунктов заголовки 3 уровня с контентом

- Пояснение что такое
- Пояснение что есть `{% block %}`  а так же `include`
- Пояснение что есть `{% extends %}`
- Рассказ про то что блоки можно переопределить, расширить или дать им значение по умолчанию

![templates_extends_schema.png](./images/templates_extends_schema.png)

## Простой пример наследования шаблонов в Django 📝

`base.html`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>
        {% block title %}
        "Барбершоп "Арбуз"
        {% endblock title %}
    </title>
</head>
<body>
    {% block content %}{% endblock content %}
</body>
</html>
```

`thanks.html`

```html
{% extends "base.html" %}
{% block content %}
    <h1>Спасибо за заявку!</h1>
    <p>Мы свяжемся с вами в ближайшее время!</p>
{% endblock content %}
```

Пример на скриншоте
![first_template_exends.png](./images/first_template_exends.png)

## Простой пример `include` в Django 📝

Тег шаблона `include` позволяет включать в шаблон другой шаблон. И делает это немного по-другому, чем `extends`.

Причем мы можем включить шаблон в блок шаблона, чтобы была возможность выключить отображение блока на той или иной странице.

Как например тут:

`include_nav_menu.html`

```html
{% comment %} nav>ul>li*5>a {% endcomment %}
<nav>
    <ul>
        <li><a href="">Текст ссылки</a></li>
        <li><a href="">Текст ссылки</a></li>
        <li><a href="">Текст ссылки</a></li>
        <li><a href="">Текст ссылки</a></li>
        <li><a href="">Текст ссылки</a></li>
    </ul>
</nav>
```

`base.html`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>
        {% block title %}
        "Барбершоп "Арбуз"
        {% endblock title %}
    </title>
</head>
<body>
    <header>
        {% block header %}
        {% include "include_nav_menu.html" %}
        {% endblock header %}
    </header>
    <main>
        {% block content %}{% endblock content %}
    </main>
    <footer>

    </footer>
    
</body>
</html>
```

- Пояснение как это работает
- Что ссылки меню и текст ссылок мы можем передавать через контекст вью
- Что мы можем выключить отображение навигационного меню определив блок в наследуемом шаблоне

## Пример с `include` в цикле шаблонизатора 📝

Мы модифицировали `orders_list.html` так, что вынесли карточку заказа в отдельный шаблон `include_order_card.html`

И сейчас это выглядит так:

`orders_list.html`

```html
    <h1>Список заявок</h1>
    <div class="flex-container">
        {% comment %} Проверка на пустую коллекцию empty{% endcomment %}
        {% for order in orders %}
        {% include "include_order_card.html" %}
        {% endfor %}
    </div>
```

`include_order_card.html`

```html
        <div class="flex-card">
            <h2>ID заявки: {{ order.id }}</h2>
            <p>Имя: {{ order.client_name }}</p>

            <p>Дата заявки: {{ order.date }}</p>
            <p class= {% if order.status == "новая" %}
            "new"
            {% elif order.status == "подтвержденная" %}
            "confirmed"
            {% elif order.status == "отмененная" %}
            "rejected"
            {% elif order.status == "выполненная" %}
            "canceled"
            {% endif %}
            >Статус заявки: {{ order.status }}</p>
            <p>Количество услуг: {{ order.services|length }}</p>
            <div class="services">
                {% comment %} цикл для span услуг {% endcomment %}
                {% for service  in order.services  %}
                <span class="service">{{ service }}</span>
                {% endfor %}
            </div>
        </div>
```

Т.е. мы вынесли flex елемет в отдельный шаблон, и рендерим его циклом внутри flex-container

## Подключение статики в Django 📝

### Подключение в базовом шаблоне

В базовый шаблон мы можем подключить BS5 стили, скрипты, иконки. 
А так же нашу статику.

Выглядить это будет как на скрине

![static_tag.png](./images/static_tag.png)

На скриншоте этого нет, но не забудьте подключить статику в первой строке базового шаблона.

`base.html`
```html
{% load static %}
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {% comment %} Подключаю 2мя ссылками BS5 и BS5 иконки {% endcomment %}
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    {% comment %} Подключаю стили {% endcomment %}
    <link rel="stylesheet" href="{% static 'css/main.css' %}">
```

А так же скрипты

```html
...
 {% comment %} Подключаю скрипты BS5 {% endcomment %}
     <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
     {% comment %} Подключаю свои скрипты {% endcomment %}
     <script src="{% static 'js/script.js' %}"></script>
</body>
```

Но для статики понадобятся дополнительные настройки.

- пояснения про то тег `{% static %}`
- пояснения что для того чтобы она раздавалась нам нужно настроить настройки + маршруты

![static_tag_2.png](./images/static_tag_2.png)

### `Settings.py` и настройка статики

Нам нужно определить 2 настройки в `settings.py`

```python
STATIC_URL = '/static/'
STATICFILES_DIR = [BASE_DIR / 'static']
```

### `urls.py` и настройка статики

В урлах нам нужно произвести импорт статики, а так же добавить маршруты для статики

```python
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    ...
    ] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

```

## Пример - как это будет выглядеть в итоге


![static_and_extends_templates.png](./images/static_and_extends_templates.png)

- Пояснения, мы можем подключить эти карточки в любое место сайта, где нам нужно

`include_order_card.html`
```html
        <div class="flex-card">
            <h2>ID заявки: {{ order.id }}</h2>
            <p>Имя: {{ order.client_name }}</p>

            <p>Дата заявки: {{ order.date }}</p>
            <p class= {% if order.status == "новая" %}
            "new"
            {% elif order.status == "подтвержденная" %}
            "confirmed"
            {% elif order.status == "отмененная" %}
            "rejected"
            {% elif order.status == "выполненная" %}
            "canceled"
            {% endif %}
            >Статус заявки: {{ order.status }}</p>
            <p>Количество услуг: {{ order.services|length }}</p>
            <div class="services">
                {% comment %} цикл для span услуг {% endcomment %}
                {% for service  in order.services  %}
                <span class="service">{{ service }}</span>
                {% endfor %}
            </div>
        </div>
```

- Пояснения - у нас нет дублирования кода, карточка вынесена отдельно, а все что надо подключено в базовом шаблоне

`orders_list.html`
```html
{% extends "base.html" %}
{% block content %}   
<h1>Список заявок</h1>
    <div class="flex-container">
        {% comment %} Проверка на пустую коллекцию empty{% endcomment %}
        {% for order in orders %}
        {% include "include_order_card.html" %}
        {% endfor %}
    </div>
{% endblock content %} 
```

- Пояснения, в базовом шаблоне мы подключаем все что надо, мы будем использвать этот шаблон как основу для других шаблонов
- В нем можно сделать и другие блоки, например для стилей и скриптов, чтобы добавить их через super в других шаблонах

`base.html`
```html
{% load static %}
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {% comment %} Подключаю 2мя ссылками BS5 и BS5 иконки {% endcomment %}
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    {% comment %} Подключаю стили {% endcomment %}
    <link rel="stylesheet" href="{% static 'css/main.css' %}">
    <title>
        {% block title %}
        "Барбершоп "Арбуз"
        {% endblock title %}
    </title>
</head>
<body>
    <header>
        {% block header %}
        {% include "include_nav_menu.html" %}
        {% endblock header %}
    </header>
    <main>
        {% block content %}{% endblock content %}
    </main>
    <footer>

    </footer>
    {% comment %} Подключаю скрипты BS5 {% endcomment %}
     <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
     {% comment %} Подключаю свои скрипты {% endcomment %}
     <script src="{% static 'js/main.js' %}"></script>
</body>
</html>
```

## Super в шаблонах

### Что такое super

### Как использовать super

## Шаблонный тег `url`

#TODO - сделать из каждого заголовок 3 уровня и добавить материал текст и краткие примеры!
- Что такое шаблонный тег `url`
- Псевдонимы маршрутов и их использование
- Как передавать параметры в url
- Как нам облагородить наше меню которое сейчас выглядит так
```html
{% comment %} nav>ul>li*5>a {% endcomment %}
<nav>
    <ul>
        <li><a href="">Текст ссылки</a></li>
        <li><a href="">Текст ссылки</a></li>
        <li><a href="">Текст ссылки</a></li>
        <li><a href="">Текст ссылки</a></li>
        <li><a href="">Текст ссылки</a></li>
    </ul>
</nav>
```
Сделаем простое меню (без определения активной страницы, и без циклов, но с использованием шаблонного тега `url`)
Чтобы можно было осуществлять навигацию по сайту и переходить на другие страницы.

Для этого нам надо будет сформировать список словарей - поместить его во `views.py` и передаавать во всех вью!

## Что такое контекстный проце

#TODO - сделать из каждого заголовок 3 уровня и добавить материал текст и краткие примеры!
- Определине контекстного процессора
- Какие уже есть контекстные процессоры и где они подключены
- Как нам описать собственный процессор и что для этого надо?
- Пример своего процессора для передачи данных меню
- Теперь мы можем убрать из всех вьюх передачу данных меню и передавать их через контекстный процессор