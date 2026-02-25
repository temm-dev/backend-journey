
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.http import HttpResponseNotFound
from .dynamodb_models import UserModel
from .forms import UserForm


class UserListView(View):
    """Список всех пользователей (через scan)."""
    def get(self, request):
        # Внимание: scan() в DynamoDB читает всю таблицу, что может быть дорого.
        # Для небольших объёмов данных и учебных целей это допустимо.
        # В реальных проектах лучше использовать query с соответствующим индексом.
        users = list(UserModel.scan())  # scan возвращает итератор, преобразуем в список
        return render(request, 'users/user_list.html', {'users': users})

class UserCreateView(View):
    """Создание нового пользователя."""
    def get(self, request):
        form = UserForm()
        return render(request, 'users/user_form.html', {'form': form, 'action': 'Создать'})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            # Создаём объект модели PynamoDB
            user = UserModel(
                user_id=form.cleaned_data['user_id'],
                email=form.cleaned_data['email'],
                full_name=form.cleaned_data.get('full_name') or None,
                age=form.cleaned_data.get('age')
            )
            # Сохраняем в DynamoDB
            user.save()
            return redirect('user_list')
        return render(request, 'users/user_form.html', {'form': form, 'action': 'Создать'})

class UserDetailView(View):
    """Детальная информация о пользователе."""
    def get(self, request, user_id):
        try:
            # Получаем объект по ключу (очень быстро)
            user = UserModel.get(user_id)
        except UserModel.DoesNotExist:
            return HttpResponseNotFound("Пользователь не найден")
        return render(request, 'users/user_detail.html', {'user': user})

class UserDeleteView(View):
    """Удаление пользователя."""
    def post(self, request, user_id):
        try:
            user = UserModel.get(user_id)
            user.delete()  # удаляем из DynamoDB
        except UserModel.DoesNotExist:
            pass  # можно проигнорировать
        return redirect('user_list')