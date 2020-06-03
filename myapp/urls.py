from django.urls import path
from . import views
from django.conf import settings

urlpatterns = []

if settings.STAGE == 'production':
    urlpatterns = [
        path('', views.home, name='homeAuth'),
        path('musicServiceAuth', views.musicServiceAuth, name='musicServiceAuth'),
        path('authRedirect', views.authRedirect, name='testing'),
        path('userTopMusic/', views.get_users_top_music, name='user-top-music')

    ]
elif settings.STAGE == 'development':
    urlpatterns = [
        path('', views.home, name='homeAuth'),
        path('playlists/', views.playlists, name='playlists'),
        path('search', views.search, name='search'),
        path('musicServiceAuth', views.musicServiceAuth, name='musicServiceAuth'),
        path('authRedirect', views.authRedirect, name='testing'),
        path('playlistData/', views.playlist_data, name='playlist-data'),
        path('addToPlaylist/', views.add_to_playlist, name='add-to-playlist'),
        path('exportPlaylist/', views.export_playlist, name='export-playlist'),
        path('userTopMusic/', views.get_users_top_music, name='user-top-music')

    ]
