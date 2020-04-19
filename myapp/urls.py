from django.urls import path
from . import views


urlpatterns = [
    path('playlists,', views.playlists, name='playlists'),
    path('search', views.search, name='search'),
    path('musicServiceAuth', views.musicServiceAuth, name='musicServiceAuth'),
    path('', views.home, name='home'),
    path('authRedirect', views.authRedirect, name='testing'),

]
