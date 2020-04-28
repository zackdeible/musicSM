from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import path
from .models import Playlist, Track, Profile
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
        #print("ALBUM", rjson['tracks']['items'][0]['album']['name'])
        #print("ARTIST",rjson['tracks']['items'][0]['artists'][0]['name'])
        #print("SONG",rjson['tracks']['items'][0]['name'])
        #print("LINK",rjson['tracks']['items'][0]['preview_url'])

        playlist = Playlist.objects.all()
        #print("user", request.user)
        #print("PLAYLISTTTTTT", playlist)

        #print(response.text.encode('utf8'))

    return render(request, 'myapp/search.html', {'searchResults':rjson, 'playlists': playlist})

def playlists(request):
    current_user = request.user
    data = Playlist.objects.all()
    #print(current_user)

    pls = {
        "playlists": data
    }


    if request.method == 'POST':
        form = request.POST
        posts = request.POST.get("playlist-name")
        playlist = Playlist(playlist_name=posts)
        playlist.save()

        #print("current", current_user)
        #print(Playlist.objects.get(playlist_name=posts))
        #playlist.users.add(current_user)
        #print(playlist.users.add(current_user))

        #playlist.save()


    return render(request, 'myapp/playlists.html', pls)

def add_to_playlist(request):

    # 1) get the track name that is selected (will eventually need to get album to search for ID)

    # 2) Get the track ID for that track

    # 3) Add that ID for each of the playlists


    if request.method == 'POST':
        data = request.POST
        print(data)

        playlists = data.getlist('playlists[]')
        for x in playlists:
            print(x)
        #print(data['playlists[]'])
    return render(request, 'myapp/playlists.html')

def playlist_data(request):
    # 1) call track db
    track = Track()

    # 2) Check if track AND album are in the db already

    # 3) If it is, do not do anything

    # 4) If it isn't save all attributes to db, an ID will be generated and the track in in our db

    if request.method == 'POST':
        print(request.POST)
        data = request.POST
        track_name = data['trackname']
        album_name = data['albumname']
        track_artist = data['trackartist']
        album_pic = data['albumpic']
        spotify_url = data['spotifyurl']



    return render(request, 'myapp/playlists.html')
