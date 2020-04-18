from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.urls import path
import requests

token = ''

# Create your views here.
def home(request):
    authCode = request.GET.get('code')

    global token
    if request.method == 'GET':
        url = "https://accounts.spotify.com/api/token"

        payload = ('grant_type=authorization_code&code='+
                    authCode +
                    '&redirect_uri=http%3A//127.0.0.1%3A8000')
        headers = {
          'Authorization': 'Basic YTk5Njg1ZjgzNWQyNDBjYjg3OTE1OGYyMTgzYmEwMDA6ODJkZmNjMzVkN2MxNGNhNzlhOGJjOGIyN2YwYmMzMzA=',
          'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data = payload)

        token = response.json()['access_token']
        print('MY TOKEN: ',token)

        print(response.text.encode('utf8'))

    return render(request, 'myapp/search.html')


def testing(request):
    return redirect('https://accounts.spotify.com/en/authorize?client_id=a99685f835d240cb879158f2183ba000&redirect_uri=http:%2F%2F127.0.0.1:8000&response_type=code')

def musicServiceAuth(request):
     return render(request, 'myapp/musicServiceAuth.html')

def search(request):
    global token

    if request.method == 'POST':
        query = request.POST['search']
        print(query)
        authToken = token
        q = query
        type = 'artist'

        query = query.replace(' ','%20')

        url = ("https://api.spotify.com/v1/search?q=" +
                q +
                '&type=' +
                type +
                '&access_token=' +
                authToken)




        response = requests.request("GET", url)

        rjson = response.json()

        print(response.text.encode('utf8'))

    return render(request, 'myapp/search.html', {'searchResults':rjson})
