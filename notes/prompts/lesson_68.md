# Тема Django - Система пользователей. Ч3 - Своя модель User . Урок 68
- Когда и зачем надо создавать новую модель пользователя
- Нельзя вот так просто взять и создать модель пользователя и накатить миграции. ПОЧЕМУ?
- А что делать? Удалить ВСЕ или только откатить служебные таблицы завязанные на пользователя
## Миграции

- Если вы начали с модели то столкнулись с ошибкой. Миграции создаются. Но применить их нельзя

`django.db.migrations.exceptions.InconsistentMigrationHistory: Migration admin.0001_initial is applied before its dependency users.0001_initial on database 'default'.`

- Проблема в том что миграции админки идут первыми и ссылаются на пользователя. А модель пользователя изменилась.

- Выходит что нам надо либо пересоздавать ВСЮ базу, либо откатывать служебные миграции и накатывать их заново!
- Поэтому лучше начать с миграций!

## Откатим служебные модели 
- Описание команд.
```bash
poetry run python manage.py migrate admin zero
poetry run python manage.py migrate auth zero
poetry run python manage.py migrate contenttypes zero
```

## Создание своей модели пользователя
- Описание работы которую делаем
```python
# users/models.py
from django.db import models

# Импорт AbstractUser
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя.
    Наследуясь от AbstractUser мы получаем все его поля и методы
    И можем быть интегрированы в Django гармонично
    """

    avatar = models.ImageField(
        upload_to="avatars", verbose_name="Аватар", null=True, blank=True
    )
    phone = models.CharField(
        max_length=20, verbose_name="Телефон", null=True, blank=True
    )
    birthday = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    vk_id = models.CharField(
        max_length=100, verbose_name="ID пользователя ВКонтакте", null=True, blank=True
    )
    tg_id = models.CharField(
        max_length=100, verbose_name="ID пользователя в Телеграм", null=True, blank=True
    )
```

#TODO Пояснения

Регистарция модели в настройках

```python
# Новая модель пользователя users.models.CustomUser 
AUTH_USER_MODEL = "users.CustomUser"
```

```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

f