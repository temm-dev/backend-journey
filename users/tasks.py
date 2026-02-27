from math import exp
import requests

from celery import shared_task
import logging
import random


logger = logging.getLogger(__name__)

@shared_task
def add(x, y):
    result = x * y
    print(f"Результат сложения {x} + {y} = {result}")
    return result

@shared_task(bind=True, max_retries=4)
def weather(self, city):
    url = f'https://wttr.in/{city}?format=%t'

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        temperature = response.text.strip()
        logger.info(f"Температура в {city}: {temperature}")
        return temperature
    except Exception as e:
        retry_num = self.request.retries + 1
        countdown = 2 ** retry_num + random.randint(0, 5)
        
        logger.warning(f"Ошибка при запросе {city}: {e}. Попытка {retry_num} из {self.max_retries}. Повтор через {countdown} сек.")
        
        raise self.retry(exc=e, countdown=countdown)