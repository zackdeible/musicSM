from django.urls import path
from . import views


urlpatterns = [
    path('search', views.search, name='search'),
    path('musicServiceAuth', views.musicServiceAuth, name='musicServiceAuth'),
    path('', views.home, name='home'),
    path('testing', views.testing, name='testing'),
]
