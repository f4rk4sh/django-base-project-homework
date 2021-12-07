from django.urls import path
from .views import UserView, UserListView, RegisterView

app_name = 'apps.authentication'

urlpatterns = [
    path('', UserView.as_view(), name='user'),
    path('users/', UserListView.as_view(), name='users'),
    path('register/', RegisterView.as_view(), name='register'),
]
