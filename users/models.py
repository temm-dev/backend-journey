# users/dynamodb_models.py
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
from datetime import datetime
from django.conf import settings

class UserModel(Model):
    """
    Модель пользователя в DynamoDB.
    Ключом является user_id (уникальный идентификатор пользователя).
    """
    class Meta:
        table_name = 'users'
        # Используем настройки из django.conf.settings
        host = settings.DYNAMODB_HOST
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
        region = settings.AWS_REGION

    # Хеш-ключ (обязательный)
    user_id = UnicodeAttribute(hash_key=True)

    # Остальные атрибуты
    email = UnicodeAttribute(null=False)          # обязательный, не может быть пустым
    full_name = UnicodeAttribute(null=True)       # может быть пустым
    age = NumberAttribute(null=True)
    created_at = UTCDateTimeAttribute(default=datetime.utcnow)

    def __str__(self):
        return f"{self.full_name or 'No name'} ({self.email})"