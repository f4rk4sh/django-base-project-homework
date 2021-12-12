from django.contrib import admin
from django.urls import path, include
from apps.authentication.views import verify

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(('django.contrib.auth.urls', 'auth'), namespace='auth')),
    path('authentication/', include('apps.authentication.urls', namespace='authentication')),
    path(r'verify/<uuid:user_id>/', verify, name='verify'),
    path('', include('apps.movies.urls', namespace='movies')),
]
















