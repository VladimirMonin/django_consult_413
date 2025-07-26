# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review
from .mistral import is_bad_review


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
        

