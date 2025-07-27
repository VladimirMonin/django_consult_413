# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review, Order
from .mistral import is_bad_review
from .telegram_bot import send_telegram_message
from django.conf import settings
import asyncio

api_key = settings.TELEGRAM_BOT_API_KEY
user_id = settings.TELEGRAM_USER_ID

@receiver(post_save, sender=Order)
def notify_telegram_on_order_create(sender, instance, created, **kwargs):
    try:
        if created and not kwargs.get('raw', False):
            tg_markdown_message = f"""

====== *Новый заказ!* ======
**Имя:** {instance.name}
**Телефон:** {instance.phone}
**Мастер:** {instance.master.name}
**Дата записи:** {instance.appointment_date}
**Услуги:** {', '.join([service.name for service in instance.services.all()])}
**Комментарий:** {instance.comment}

**Подробнее:** http://127.0.0.1:8000/admin/core/order/{instance.id}/change/

#заказ

"""
            asyncio.run(send_telegram_message(api_key, user_id, tg_markdown_message))
    except Exception as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")


@receiver(post_save, sender=Review)
def ai_validate_process_review(sender, instance, created, **kwargs):
    # Была ли создана новая запись и не является ли это raw - записью из фикстур
    if created and not kwargs.get('raw', False):
        # Меняем статус "На модерации"
        instance.status = "ai_moderating"

        # Запускаем валидацию через AI - возвращает True или False
        try:
            is_bad = is_bad_review(instance.text)
            if is_bad:
                instance.status = "ai_rejected"
            else:
                instance.status = "ai_approved"

        except Exception as e:
            print(f"Ошибка при проверке отзыва: {e}")

        finally:
            instance.save()