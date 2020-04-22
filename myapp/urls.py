from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('playlists/', views.playlists),
    path('search', views.search, name='search'),
    path('musicServiceAuth', views.musicServiceAuth, name='musicServiceAuth'),
    path('authRedirect', views.authRedirect, name='testing'),

]
