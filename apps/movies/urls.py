from django.urls import path
from .views import MovieListView, MovieDetailView, MovieCreateView, MovieUpdateView, PersonCreateView, RatingView, LongRunningView

app_name = 'apps.movies'

urlpatterns = [
    path('', MovieListView.as_view(), name='movie_list'),
    path(r'<int:pk>/', MovieDetailView.as_view(), name='movie_details'),
    path(r'add/movie/', MovieCreateView.as_view(), name='movie_add'),
    path(r'update/movie/<int:pk>', MovieUpdateView.as_view(), name='movie_update'),
    path(r'add/person/', PersonCreateView.as_view(), name='person_add'),
    path('rating/', RatingView.as_view(), name='rating'),
    path('long_running/', LongRunningView.as_view(), name='long_running'),
]
