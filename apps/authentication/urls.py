from django.urls import path
from .views import UserView, UserListView, SignUpView, ActivateView

app_name = 'apps.authentication'

urlpatterns = [
    path('', UserView.as_view(), name='user'),
    path('users/', UserListView.as_view(), name='users'),
    path('register/', SignUpView.as_view(), name='register'),
    path(r'activate/<str:uidb64>/<str:token>/', ActivateView.as_view(), name='activate')
]
