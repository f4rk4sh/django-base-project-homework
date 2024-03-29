from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.movies.models import Movie, Person
from .forms import MovieForm, PersonForm
from django.urls import reverse_lazy
from django.db import connection
from django.http import HttpResponse
from time import sleep
import logging


logger = logging.getLogger(__name__)


class SearchMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(name__icontains=self.request.GET.get('q', ''))


class MovieListView(SearchMixin, ListView):
    template_name = 'movies/list.html'
    model = Movie
    context_object_name = 'movies'
    paginate_by = 20


class MovieDetailView(DetailView):
    template_name = 'movies/detail.html'
    model = Movie
    context_object_name = 'movie'


class MovieCreateView(LoginRequiredMixin, CreateView):
    template_name = 'movies/add_movie.html'
    model = Movie
    form_class = MovieForm

    def get_success_url(self):
        return reverse_lazy('movies:movie_details', kwargs={'pk': self.object.pk})


class MovieUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'movies/update_movie.html'
    model = Movie
    form_class = MovieForm

    def get_success_url(self):
        return reverse_lazy('movies:movie_details', kwargs={'pk': self.object.pk})


class PersonCreateView(LoginRequiredMixin, CreateView):
    template_name = 'movies/add_person.html'
    model = Person
    form_class = PersonForm
    success_url = reverse_lazy('movies:movie_list')


class RatingView(TemplateView):
    template_name = 'movies/rating.html'

    @staticmethod
    def actors_rating():
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT movies_person.name, sum(sq.rating) as rating from movies_person
                join movies_personmovie on movies_personmovie.person_id = movies_person.id
                join (Select movies_movie.id as "movie_id", sum(sq.rating) as rating from movies_movie
                join movies_personmovie on movies_personmovie.movie_id = movies_movie.id
                join (Select movies_person.id AS "person_id", count(*) as rating from movies_person
                join public.movies_personmovie on movies_person.id = movies_personmovie.person_id
                where
                    movies_personmovie.category = 'actor' or
                    movies_personmovie.category = 'actress' or
                    movies_personmovie.category = 'self'  
                group by movies_person.id) as sq on sq.person_id = movies_personmovie.person_id
                group by movies_movie.id) as sq on sq.movie_id = movies_personmovie.movie_id
                where
                    movies_personmovie.category = 'actor' or
                    movies_personmovie.category = 'actress' or
                    movies_personmovie.category = 'self'
                group by movies_person.name
                order by rating DESC;
            ''')
            all_actors_rating = cursor.fetchall()
        actors_rating = all_actors_rating[:10]
        return actors_rating

    @staticmethod
    def movies_rating():
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT movies_movie.name, sum(sq.rating) as rating from movies_movie
                join movies_personmovie on movies_personmovie.movie_id = movies_movie.id
                join (Select movies_person.id AS "person_id", count(*) as rating from movies_person
                left outer join public.movies_personmovie on movies_person.id = movies_personmovie.person_id
                where
                    movies_personmovie.category = 'actor' or
                    movies_personmovie.category = 'actress' or
                    movies_personmovie.category = 'self'  
                group by movies_person.id) as sq on sq.person_id = movies_personmovie.person_id
                group by movies_movie.id
                order by rating desc;
            ''')
            all_movies_rating = cursor.fetchall()
        movies_rating = all_movies_rating[:10]
        return movies_rating

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['actors_rating'] = self.actors_rating()
        context['movies_rating'] = self.movies_rating()
        return context


class LongRunningView(View):
    @staticmethod
    def get(request):
        logger.error('starting...')
        sleep(10)
        logger.error('Ok')
        return HttpResponse('Ok')
