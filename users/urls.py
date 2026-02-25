# users/urls.py
from django.urls import path
from .views import UserListView, UserCreateView, UserDetailView, UserDeleteView

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('new/', UserCreateView.as_view(), name='user_create'),
    path('<str:user_id>/', UserDetailView.as_view(), name='user_detail'),
    path('<str:user_id>/delete/', UserDeleteView.as_view(), name='user_delete'),
]