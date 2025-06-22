# Тема Django. Наследование шаблонов. Include. Контекстный процессор. Урок 53

## Что такое наследование шаблонов в Django? 🤔

# TODO Сделать из этих пунктов заголовки 3 уровня

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
