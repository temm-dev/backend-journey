# users/forms.py
from django import forms

class UserForm(forms.Form):
    # Поля формы соответствуют атрибутам модели UserModel
    user_id = forms.CharField(
        max_length=128,
        label='User ID',
        help_text='Уникальный идентификатор пользователя (например, логин или UUID)'
    )
    email = forms.EmailField(label='Email')
    full_name = forms.CharField(
        max_length=255,
        required=False,
        label='Полное имя'
    )
    age = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=150,
        label='Возраст'
    )