from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='homeAuth'),
    path('playlists/', views.playlists, name='playlists'),
    path('search', views.search, name='search'),
    path('musicServiceAuth', views.musicServiceAuth, name='musicServiceAuth'),
    path('authRedirect', views.authRedirect, name='testing'),
    path('playlistData/', views.playlist_data, name='playlist-data'),
    path('addToPlaylist/', views.add_to_playlist, name='add-to-playlist')

]
