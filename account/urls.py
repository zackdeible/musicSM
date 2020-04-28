from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.login_request, name='account-login'),
    path('register/', views.register, name='account-register'),
    path('logout/', views.logout_request, name='account-logout')

]
