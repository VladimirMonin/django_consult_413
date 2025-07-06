## План работ и коммитов  

НЕ ЗАБЫВАЙ ПРО BS5 иконки!

| № | Что делаем | Файлы | Сообщение коммита |
|---|------------|-------|-------------------|
| 1 | Подключаем Google Fonts, обновляем `<head>` | `templates/base.html` | `feat: подключены шрифты Cormorant Garamond и Fira Sans` |
| 2 | Создаём include карточки мастеров, услуг, отзывов | `templates/include_master_card.html`, `include_service_card.html`, `include_reviews_carousel.html` | `feat: добавлены include-шаблоны карточек мастеров, услуг и отзывов` |
| 3 | Полная разметка секций лендинга | `templates/landing.html` | `feat: верстка лендинга согласно концепции` |
| 4 | Обновляем меню (иконки, якоря, пункты staff) | `templates/include_nav_menu.html`, `core/context_processors.py` | `feat: расширено меню, добавлен пункт "Список услуг" для персонала` |
| 5 | CSS: переменные, карточки, sticky footer | `static/css/main.css` | `style: ретро-стили и фиксированный подвал` |
| 6 | JS: плавный скролл | `static/js/main.js` | `feat: добавлен плавный скролл по якорям` |
| 7 | Создаём `OrderForm`, view `order_create`, AJAX-скрипт | `core/forms.py`, `core/views.py`, `static/js/order_form.js`, `templates/include_order_form.html`, `barbershop/urls.py` | `feat: форма заявки, AJAX-отправка и обработка` |
| 8 | Выводим мастеров, услуги, отзывы в контекст | `core/views.py` | `feat: передача мастеров, услуг и отзывов в шаблон` |
| 9 | Страница списка услуг для персонала | `core/views.py`, `templates/services_list.html` | `feat: страница списка услуг (доступ staff)` |
|10 | Адаптивность и финальное тестирование | разн. | `chore: проверка адаптивности и мелкие правки` |
# Барбершоп «Арбуз»  
**Bootstrap 5 · Ретро-стиль начала XX века (Царская Россия)**  

> Документ описывает визуальную концепцию, структуру лендинга и перечень технических задач для перехода на BS5 иконки, стили и создание единообразного облика проекта.

---

## 0. Анализ существующих моделей `core/models.py`

```text
Order   1 --- *  Service   (ManyToMany)
Order   * --- 1  Master    (FK, nullable)
Master  * --- * Service    (ManyToMany)
```

| Модель | Важные поля | Особенности |
|--------|-------------|-------------|
| `Order` | `name`, `phone`, `comment`, `status`, `appointment_date`, `services (M2M)`, `master (FK)` | `status` выбирается из `STATUS_CHOICES`; даты `auto_now_add/auto_now` |
| `Master` | `name`, `photo`, `phone`, `experience`, `is_active`, `services (M2M)` | Фото хранится в `media/masters/`, флаг активности |
| `Service` | `name`, `description`, `price`, `duration`, `is_popular`, `image` | Популярные услуги помечаются булевым признаком |

**Импликации для формы `OrderForm`:**
1. Поле `services` — `ModelMultipleChoiceField` (cрибежит из `Service`), виджет `CheckboxSelectMultiple` **или** drop-down, если нужно выбрать одну услугу.  
2. `master` не заполняется клиентом, назначается администратором позднее (оставляем `null`).  
3. Поле `status` не отображается, задаётся значением `"new"` при сохранении.  
4. При сохранении формы надо вызвать `order.services.set(...)`, если использован `commit=False`.  

**Корректировки раздела 11**  
– В форме добавим `services` как множественный выбор (checkbox-grid).  
– В обработчике `order_create` после `form.save()` добавим присвоение `services` из cleaned_data.  
– В блоке «Карточка заявки» (`include_order_card.html`) уже корректно выводятся `order.services.all`, оставляем без изменений.  
## 1. Общие визуальные принципы
| Категория | Выбор | Примечание |
|-----------|-------|------------|
| Цветовая палитра | `#704214` (сепия), `#0f5132` (изумруд), `#c79b3c` (золото), `#f8f4ec` (светлый фон) | Создают аутентичное «дореволюционное» настроение |
| Типографика | [Cormorant Garamond](https://fonts.google.com/specimen/Cormorant+Garamond) — заголовки,  <br> [Fira Sans](https://fonts.google.com/specimen/Fira+Sans) — основной текст | Обе гарнитуры имеют полную кириллицу |
| Иконки | [Bootstrap Icons 1.11](https://icons.getbootstrap.com) | Уже подключены в `base.html` |
| Сетка | Стандартная 12-колоночная BS5 | Используем `container` / `container-fluid` |

```css
/* Основные CSS-переменные: */
:root{
  --bs-body-bg:#f8f4ec;
  --bs-body-font-family:'Fira Sans', sans-serif;
  --brand-gold:#c79b3c;
  --brand-green:#0f5132;
}
```

---

## 2. Архитектура страницы `landing.html`

```mermaid
flowchart LR
#### 3.1 Кнопки для персонала (показываются, если `user.is_staff`)

| Anchor / URL | Текст | Icon | Видна кому |
|--------------|-------|------|-----------|
| `/services/` | Список услуг | `bi-list-check` | Только персонал |
| `/orders/` | Заявки | `bi-clipboard-data` | Только персонал |

В `include_nav_menu.html` эти элементы уже выводятся циклом `menu_staff_items`; просто расширяем контекст-процессор `core/context_processors.py`:

```python
menu_staff = [
    {"title": "Заявки", "url": reverse("orders")},
    {"title": "Список услуг", "url": reverse("services-list")},  # new
]
> **Важно:** файл [`templates/include_nav_menu.html`](templates/include_nav_menu.html:1) **остаётся без изменений** –  
> два существующих цикла (`menu_items` и `menu_staff_items`) продолжают работать,  
> мы лишь расширили `menu_staff_items` вторым словарём. Структура контекст-процессора и шаблона сохранена.
```

И добавляем маршрут `services-list` (позже реализуем).  
Так навигация останется полной для персонала и не упростит проект.  
  A(Hero) --> B(Мастера)
  B --> C(Услуги)
  C --> D(Отзывы)
  D --> E(Форма записи)
```

| Секция | id | Шаблон / include | Ключевые BS5-классы | Описание |
|--------|----|------------------|---------------------|----------|
| Hero | `top` | — | `row align-items-center py-5` | Слева слоган и CTA-кнопка, справа фото `barber.webp` |
| Мастера | `masters` | `include_master_card.html` | `row row-cols-1 row-cols-md-2 row-cols-lg-4 g-4` | Карточки мастеров |
| Услуги | `services` | `include_service_card.html` | `row row-cols-1 row-cols-md-3 g-4` | Группируем по категориям (см. §4) |
| Отзывы | `reviews` | `include_reviews_carousel.html` | `carousel slide` | 3–5 отзывов |
| Форма записи | `get-order` | — | `bg-light p-5 rounded` | Форма: имя, телефон, выбор услуги, дата |

---

## 3. Навигация `include_nav_menu.html`

| Anchor | Текст | Icon | Доп. класс |
|--------|-------|------|-----------|
| `#top` | Главная | `bi-house` | — |
| `#masters` | Мастера | `bi-person-badge` | — |
| `#services` | Услуги | `bi-scissors` | — |
| `#reviews` | Отзывы | `bi-chat-dots` | — |
| `#get-order` | Записаться | `bi-calendar-check` | `btn btn-success ms-lg-3` |

---

## 4. Услуги и карточки

### 4.1. Категории
1. **Стрижки**  
   * Мужская классическая  
   * Стрижка машинкой  
   * Стрижка бороды  
2. **Бритьё**  
   * Королевское бритьё опасной бритвой  
3. **Уход**  
   * Мытьё головы + укладка  
   * Масло для бороды  

### 4.2. Шаблон `include_service_card.html`
```html
<div class="col">
  <div class="card h-100 text-center position-relative">
    {% if service.is_popular %}
      <span class="badge bg-warning position-absolute top-0 end-0">Хит</span>
    {% endif %}
    <img src="{{ service.image.url|default:'/static/images/default_service.png' }}"
         class="card-img-top" alt="{{ service.name }}">
    <div class="card-body">
      <h5 class="card-title">{{ service.name }}</h5>
      <p class="card-text">{{ service.description|truncatewords:12 }}</p>
    </div>
    <div class="card-footer">
      <span class="fw-bold">{{ service.price }} ₽</span>
    </div>
  </div>
</div>
```
**Стили:**
```css
.card{
  border:2px solid var(--brand-gold);
  box-shadow:0 2px 6px rgba(0,0,0,.08);
}
```

---

## 5. Карточка мастера `include_master_card.html`
```html
<div class="col">
  <div class="card text-center h-100">
    <img src="{{ master.photo.url|default:'/static/images/default_master.png' }}"
         class="rounded-circle mx-auto d-block mt-3" style="width:120px;height:120px;" alt="{{ master.name }}">
    <div class="card-body">
      <h5 class="card-title">{{ master.name }}</h5>
      <p class="card-text text-muted">Опыт: {{ master.experience }} лет</p>
      <div>
        {% for srv in master.services.all %}
          <i class="bi bi-scissors text-secondary"></i>
        {% endfor %}
      </div>
    </div>
  </div>
</div>
```

---

## 6. Отзывы `include_reviews_carousel.html`
Стандартный BS5 Carousel внутри `col-md-8 mx-auto`. Каждому отзыву — цитата, имя клиента, дата.

---

## 7. Footer (sticky)
```html
<footer class="footer-dark mt-auto">
  <div class="container text-center text-md-start">
    <div class="row">
      <div class="col-md-4 mb-3">
        <h5 class="mb-3">Барбершоп «Арбуз»</h5>
        <p>г. Петербург, Невский пр., 42</p>
        <p>Ежедневно 10:00-22:00</p>
      </div>
      <div class="col-md-4 mb-3">
        <h5 class="mb-3">Контакты</h5>
        <p><i class="bi bi-telephone"></i> +7 900 000-00-00</p>
        <p><i class="bi bi-envelope"></i> hello@arbuz.barber</p>
      </div>
      <div class="col-md-4 mb-3">
        <h5 class="mb-3">Мы в соцсетях</h5>
        <a class="text-white me-2" href="#"><i class="bi bi-instagram"></i></a>
        <a class="text-white me-2" href="#"><i class="bi bi-telegram"></i></a>
        <a class="text-white" href="#"><i class="bi bi-vk"></i></a>
      </div>
    </div>
  </div>
</footer>
```

```css
.footer-dark{
  background:var(--brand-green);
  color:#fff;
  padding:2rem 0;
}
```

---

## 8. JavaScript (`static/js/main.js`)
```js
/* Плавный скролл по якорям */
document.querySelectorAll('a[href^="#"]').forEach(link=>{
  link.addEventListener('click', e=>{
    e.preventDefault();
    document.querySelector(link.getAttribute('href'))
            .scrollIntoView({behavior:'smooth', block:'start'});
  });
});
```

---

## 9. Перечень задач для реализации ↓

| № | Задача | Файл/директория |
|---|--------|-----------------|
| 1 | Подключить Google Fonts (2 семейства) | `templates/base.html` |
| 2 | Создать include-файлы: `include_master_card.html`, `include_service_card.html`, `include_reviews_carousel.html` | `templates/` |
| 3 | Разметить секции `landing.html` согласно §2 | `templates/landing.html` |
| 4 | Обновить меню якорями + стили | `templates/include_nav_menu.html` |
| 5 | Добавить/обновить CSS (переменные, карточки, footer, sticky body) | `static/css/main.css` |
| 6 | Дописать JS для плавного скролла | `static/js/main.js` |
| 7 | Обновить модели/контекст, чтобы передавать `masters`, `services`, `reviews` | `core/views.py` |
| 8 | Проверить адаптивность (xs-xl) | — |
| 9 | Подготовить изображения (формат WebP, 4:3) | `static/images/` |

---

## 10. Дополнительные рекомендации
* **SEO**: заполнить `<meta description>` на главной.  
* **Accessibility**: у всех img — `alt`.  
* **Performance**: минифицировать CSS/JS в production, использовать `loading="lazy"` для картинок.  

---

**После выполнения задач страница визуально соответствует ретро-стилю, а подвал всегда фиксирован внизу даже при малом контенте.**  
---

## 11. Формы и обработка заявок

### 11.1 Django `OrderForm`
| Поле | Тип | Виджет | Особенности |
|------|-----|--------|-------------|
| `name` | `CharField` | `TextInput` | `placeholder="Ваше имя"` |
| `phone` | `CharField` | `TextInput` | Regex `^\\+?7\\d{10}$`, help-text |
| `service` | `ModelChoiceField` | `Select` | queryset `Service.objects.all()` |
| `appointment_date` | `DateTimeField` | `DateInput (type=date)` | min — сегодняшняя дата |

`ModelForm` наследуется от `Order`; поле `status` устанавливается автоматически (`new`).

### 11.2 Представление
* **CBV `OrderCreateView`** (`CreateView`)  
  * `template_name = 'include_order_form.html'` (используется в секции `get-order`).  
  * `success_url = reverse_lazy('thanks')`.
* Валидная заявка сохраняет объект `Order`, затем выполняет `messages.success` и редирект.
* При AJAX-отправке возвращает JSON `{success:true}` для показа toast-уведомления.

### 11.3 URL
```python
# barbershop/urls.py
path('order/create/', OrderCreateView.as_view(), name='order-create')
```

### 11.4 Шаблон формы
```html
<form id="order-form" method="post" action="{% url 'order-create' %}" class="row g-3">
  {% csrf_token %}
  {{ form.non_field_errors }}
  <div class="col-md-6">{{ form.name }}</div>
  <div class="col-md-6">{{ form.phone }}</div>
  <div class="col-md-6">{{ form.service }}</div>
  <div class="col-md-6">{{ form.appointment_date }}</div>
  <div class="col-12 text-center">
    <button class="btn btn-success px-5" type="submit">Записаться</button>
  </div>
</form>
<script src="{% static 'js/order_form.js' %}"></script>
```

### 11.5 JavaScript `static/js/order_form.js`
Отправляет форму через `fetch`, показывает BS5 `Toast` при успехе и сбрасывает поля.

```js
document.addEventListener('DOMContentLoaded',()=>{
  const form=document.getElementById('order-form');
  form?.addEventListener('submit',async e=>{
    e.preventDefault();
    const resp=await fetch(form.action,{method:'POST',body:new FormData(form)});
    if(resp.ok){
      const toast=new bootstrap.Toast(document.getElementById('order-toast'));
      toast.show();
      form.reset();
    }
  });
});
```

---

## 9. Перечень задач для реализации (обновлено)

| № | Задача | Файл/директория |
|---|--------|-----------------|
| 1 | Подключить Google Fonts | `templates/base.html` |
| 2 | Include-шаблоны: мастера, услуги, отзывы | `templates/` |
| 3 | Разметить секции `landing.html` | `templates/landing.html` |
| 4 | Обновить меню и стили | `templates/include_nav_menu.html`, `static/css/main.css` |
| 5 | Sticky footer, переменные CSS | `static/css/main.css` |
| 6 | JS плавный скролл | `static/js/main.js` |
| 7 | **Создать `OrderForm`, `OrderCreateView`, AJAX-логика** | `core/forms.py`, `core/views.py`, `static/js/order_form.js`, `templates/include_order_form.html`, `barbershop/urls.py` |
| 8 | Передавать `masters`, `services`, `reviews` в контекст | `core/views.py` |
| 9 | Проверить адаптивность | — |
| 10 | Подготовить изображения | `static/images/` |
### 11.6 Функциональное представление (поддерживаем текущий стиль кода)

> Так как в проекте уже используются **функциональные view**, сохраняем единообразие.

```python
# core/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderForm

def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Заявка отправлена!")
            return redirect("thanks")
    else:
        form = OrderForm()
    return render(request, "include_order_form.html", {"form": form})
```

* **URL**  
  ```python
  # barbershop/urls.py
  path("order/create/", order_create, name="order-create")
  ```

* **AJAX-режим**: если заголовок `HTTP_X_REQUESTED_WITH == "XMLHttpRequest"`, возвращаем JSON `{ "success": True }`.

#### Обновление списка задач

| № | Задача | Файл |
|---|--------|------|
| 7 | **Создать `OrderForm`, функциональный view `order_create`, AJAX-логика** | `core/forms.py`, `core/views.py`, `static/js/order_form.js`, `templates/include_order_form.html`, `barbershop/urls.py` |