from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(('django.contrib.auth.urls', 'auth'), namespace='auth')),
    path('authentication/', include('apps.authentication.urls', namespace='authentication')),
    path('', include('apps.movies.urls', namespace='movies')),
]
















