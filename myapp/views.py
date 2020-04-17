from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def home(request):
     return render(request, 'myapp/search.html')


def testing(request):
    return redirect('https://accounts.spotify.com/en/authorize?client_id=a99685f835d240cb879158f2183ba000&redirect_uri=http:%2F%2F127.0.0.1:8000&response_type=code')

def musicServiceAuth(request):
     return render(request, 'myapp/musicServiceAuth.html')
