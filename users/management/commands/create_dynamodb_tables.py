# users/management/commands/create_dynamodb_tables.py
from django.core.management.base import BaseCommand
from users.dynamodb_models import UserModel

class Command(BaseCommand):
    help = 'Creates DynamoDB tables for the users app'

    def handle(self, *args, **options):
        # Проверяем, существует ли таблица
        if not UserModel.exists():
            # Создаём таблицу с минимальной пропускной способностью (для разработки)
            # wait=True — дождаться завершения создания
            UserModel.create_table(
                read_capacity_units=1,
                write_capacity_units=1,
                wait=True
            )
            self.stdout.write(self.style.SUCCESS('Table "users" created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Table "users" already exists'))