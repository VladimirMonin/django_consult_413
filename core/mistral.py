# импорт из настроек MISTRAL_MODERATIONS_GRADES
from barbershop.settings import MISTRAL_MODERATIONS_GRADES, MISTRAL_API_KEY
import os
from dotenv import load_dotenv
from mistralai import Mistral
from pprint import pprint
import time


def is_bad_review(review_text: str, api_key: str= MISTRAL_API_KEY, grades:dict =MISTRAL_MODERATIONS_GRADES) -> bool:
    # Создаем клиента Mistral с переданным API ключом
    client = Mistral(api_key=api_key)

    # Формируем запрос
    response = client.classifiers.moderate_chat(
        model="mistral-moderation-latest",
        inputs=[{"role": "user", "content": review_text}],
    )
    # Вытаскиваем данные с оценкой
    result = response.results[0].category_scores

    # Округляем значения до двух знаков после запятой
    result = {key: round(value, 3) for key, value in result.items()}

    pprint(result)

    # Словарь под результаты проверки
    checked_result = {}

    for key, value in result.items():
        if key in grades:
            checked_result[key] = value >= grades[key]

    # Если одно из значений True, то отзыв не проходит модерацию

    # тестовый слип 10 секунд
    time.sleep(10)
    return any(checked_result.values())