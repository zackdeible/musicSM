from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.urls import path
import requests, json

token = ''

# Create your views here.


def home(request):
    # Get the token code in the url
    authCode = request.GET.get('code')

    if authCode != None:

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
            print("---------------------",token)
            return render(request, 'myapp/search.html')

    else:
        return render(request, 'myapp/musicServiceAuth.html')

def authRedirect(request):
    return redirect('https://accounts.spotify.com/en/authorize?client_id=a99685f835d240cb879158f2183ba000&redirect_uri=http:%2F%2F127.0.0.1:8000&response_type=code')

def musicServiceAuth(request):
     return render(request, 'myapp/musicServiceAuth.html')

def search(request):
    global token

    if request.method == 'POST':
        query = request.POST['search']
        authToken = token
        q = query
        type = 'track'

        query = query.replace(' ','%20')

        url = ("https://api.spotify.com/v1/search?q=" +
                q +
                '&type=' +
                type +
                '&access_token=' +
                authToken)

        response = requests.request("GET", url)

        rjson = response.json()
        #tracks = rjson['tracks']
        #items = tracks['items']
        #position = items[0]
        #print("yooooo",tracks)
        #print("DICKKKKKK", items)
        #print("----------------------------------", position)
        #print("TEST", rjson['tracks']['items'][0]['album']['name'])

        #print("-------------",rjson['tracks'].items)
        print("ALBUM", rjson['tracks']['items'][0]['album']['name'])
        print("ARTIST",rjson['tracks']['items'][0]['artists'][0]['name'])
        print("SONG",rjson['tracks']['items'][0]['name'])
        print("LINK",rjson['tracks']['items'][0]['preview_url'])

        #print(response.text.encode('utf8'))

    return render(request, 'myapp/search.html', {'searchResults':rjson})

def playlists(request):
    return render(request, 'myapp/playlists.html')
