from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.login_request, name='account-login'),
    path('register/', views.register, name='account-register'),
    path('logout/', views.logout_request, name='account-logout'),
    path('users/', views.get_users, name='users'),
    path('follow/', views.follow, name='follow'),
    path('unfollow/', views.unfollow, name='unfollow'),
    path('editProfile/', views.edit_profile, name='editProfile'),
    path('changeDescription/', views.change_description, name='changeDescription'),
    path('createPost/', views.create_post, name='createPost'),
    path('savePost/', views.save_post, name='savePost'),
    path('feed/', views.feed, name='feed'),
    path('generateTopSongs/', views.generate_top_songs, name='generateTopSongs'),
    path('searchSongs/', views.search_songs, name='searchSongs'),
    path('search/', views.search, name='search')

]
