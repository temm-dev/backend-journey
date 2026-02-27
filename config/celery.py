import os
from celery import Celery

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE по умолчанию
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создаём экземпляр приложения Celery
app = Celery('config')

# Загружаем конфигурацию из настроек Django, используя пространство имён 'CELERY'
# Это значит, что все настройки Celery в settings.py должны начинаться с CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически ищем задачи в файлах tasks.py каждого установленного приложения
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')