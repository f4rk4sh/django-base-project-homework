from django.urls import path
from .views import UserView, UserListView, signup, activate

app_name = 'apps.authentication'

urlpatterns = [
    path('', UserView.as_view(), name='user'),
    path('users/', UserListView.as_view(), name='users'),
    path('register/', signup, name='register'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate')
]
