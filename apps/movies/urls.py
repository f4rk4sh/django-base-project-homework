from django.urls import path
from .views import movie_list, long_running, movie_details, movie_add

app_name = 'apps.movies'

urlpatterns = [
    path('', movie_list, name='movie_list'),
    path(r'<int:id>/', movie_details, name='movie_details'),
    path(r'add/', movie_add, name='movie_add'),
    path('long_running/', long_running, name='long_running'),
]
