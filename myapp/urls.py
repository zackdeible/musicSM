from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('testing', views.testing, name='testing'),
    path('musicServiceAuth', views.musicServiceAuth, name='musicServiceAuth')
]
