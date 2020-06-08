from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import path
import urllib.parse
from .models import Playlist, Track, Profile
import requests, json

from django.conf import settings

global_token = ''
authCode = ''

def getValidToken():
    global authCode
    print("WHAT IS THIS CODE", authCode)
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
    global global_token
    global_token = token
    return token

# Create your views here.
def home(request):
    # Get the token code in the url
    ## TODO: make this not horrible
    global authCode
    authCode = request.GET.get('code')

    if authCode != None:
        print("AUTHCODE", authCode)
        if request.method == 'GET':
            return redirect('/userTopMusic')#render(request, 'myapp/userTopMusic.html')

    else:
        return render(request, 'myapp/musicServiceAuth.html')

def authRedirect(request):
    scope = str('user-top-read playlist-modify-public')
    redirectUrl = ''
    if settings.STAGE == 'development':
        redirectUrl = urllib.parse.quote_plus(settings.DEVELOPMENT_AUTH_REDIRECT)
    elif settings.STAGE == 'production':
        redirectUrl = urllib.parse.quote_plus(settings.PRODUCTION_AUTH_REDIRECT)

    clientId = settings.SOCIAL_AUTH_SPOTIFY_KEY
    print(redirectUrl, "------------------------")
    redirectFullUrl = 'https://accounts.spotify.com/en/authorize?client_id='+clientId+'&redirect_uri='+redirectUrl+'&response_type=code&scope='+scope
    print(redirectFullUrl)
    return redirect(redirectFullUrl)

def musicServiceAuth(request):
     return render(request, 'myapp/musicServiceAuth.html')

def search(request):
    token = getValidToken()

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

        current_user = request.user
        playlist = Playlist.objects.filter(users=current_user)
        #print("user", request.user)
        #print("PLAYLISTTTTTT", playlist)

        #print(response.text.encode('utf8'))

    return render(request, 'myapp/search.html', {'searchResults':rjson, 'playlists': playlist})

#saves a playlist
def playlists(request):
    current_user = request.user
    data = Playlist.objects.filter(users=current_user)
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
        playlist.users.add(current_user)
        #print(playlist.users.add(current_user))

        playlist.save()


    return render(request, 'myapp/playlists.html', pls)

def add_to_playlist(request):

    # 1) get the track name that is selected

    # 2) Get the track ID for that track

    # 3) Add that ID for each of the playlists


    if request.method == 'POST':
        data = request.POST
        print(data)
        trackname = data['trackname']
        track = Track.objects.filter(track_name=trackname).values()
        print("----------------------------------------", track)
        for item in track:
            id = item['id']



        playlists = data.getlist('playlists[]')
        for x in playlists:
            #playlist = Playlist(playlist_name=x)
            playlist = Playlist.objects.get(playlist_name=x)
            print(playlist)
            playlist.tracks.add(id)
            playlist.save()

        #print(data['playlists[]'])
    return render(request, 'myapp/playlists.html')

def playlist_data(request):


    if request.method == 'POST':
        print(request.POST)
        data = request.POST
        track_name = data['trackname']
        album_name = data['albumname']
        track_artist = data['trackartist']
        album_pic = data['albumpic']
        spotify_url = data['spotifyurl']

        # 2) Check if track AND album are in the db already




        track_in_db = Track.objects.filter(track_name=track_name)

        if not track_in_db:
            track = Track(track_name=track_name, album_name=album_name, artist_name=track_artist, album_pic=album_pic, spotify_url=spotify_url, apple_url="")
            track.save()


        # 3) If it is, do not do anything

        # 4) If it isn't save all attributes to db, an ID will be generated and the track in in our db



    return render(request, 'myapp/playlists.html')

def export_playlist(request):

    # 1) get auth TOKEN
    # 2) get userprofile of current user
    # 3) create (POST) playlist with: https://api.spotify.com/v1/users/{user_id}/playlists
    # 3.1) look up all the songs of that playlist name, get the spotify ids in a list format
    # 4) add tracks to that playlist with: https://api.spotify.com/v1/playlists/{playlist_id}/tracks

    #token = getValidToken()
    global global_token
    token = global_token
    #print("WE MADE IT HERE BBY")
    if request.method=='POST':
        print("REQUEST.POST", request.POST)
        playlist_name = request.POST.get("searchResults")
        print("NAMEE", playlist_name)






    authToken = token
    #print("TOKEN",token)

    url_login = ('https://api.spotify.com/v1/me?access_token=' +        authToken)

    #print("URL", url)

    response = requests.request("GET", url_login)
    rjson = response.json()
    #print("THIS THE RESPONSE BITCH", rjson)

    user_id = rjson['id']
    #print("USER PROFILE", user_id)

    #create_playlist_url = ('https://api.spotify.com/v1/users/{'+user_id+'}/playlists')

    playlist_name = "TestingAgain"

    url = "https://api.spotify.com/v1/users/"+user_id+"/playlists"

    payload = "{\n    \"name\": \""+playlist_name+"\"\n}"
    headers = {
    'content-type': 'application/json',
    'Authorization': 'Bearer '+authToken,
    'Content-Type': 'text/plain',
    'Cookie': 'sp_m=us; sp_t=7e695c87-b1ef-491a-bd88-7df6fab9e443; spot=%7B%22t%22%3A1587238554%2C%22m%22%3A%22us%22%2C%22p%22%3Anull%7D'
    }

    #create_playlist = requests.request("POST", url, headers=headers, data = payload)

    #print(create_playlist.text.encode('utf8'))

    ######## get songs to add to playlists




    return render(request, 'myapp/extractPlaylist.html')


def get_users_top_music(request):

    token = getValidToken()

    authToken = token
    headers = {
      'Authorization': 'Bearer '+authToken
    }

    print("HEADERS",headers)

    # get users top tracks frin the personalization endpoint

    url_tracks = ('https://api.spotify.com/v1/me/top/tracks?limit=5&time_range=short_term')
    print(url_tracks)

    response = requests.request("GET", url_tracks, headers=headers)

    rjson = response.json()

    url_artists = ('https://api.spotify.com/v1/me/top/artists?limit=5&time_range=short_term')
    print(url_artists)

    response1 = requests.request("GET", url_artists, headers=headers)

    artist_rjson = response1.json()






    return render(request, 'myapp/userTopMusic.html', {'searchResults': rjson, 'artists': artist_rjson})

# Render top artist page
def get_users_top_artists(request):
    global global_token

    authToken = global_token

    print("--------------", authToken)
    headers = {
      'Authorization': 'Bearer '+authToken
    }

    url_artists = ('https://api.spotify.com/v1/me/top/artists?limit=5&time_range=short_term')


    response1 = requests.request("GET", url_artists, headers=headers)

    artist_rjson = response1.json()
    print("ARTISTS", artist_rjson)

    return render(request, 'myapp/topArtists.html', {'artists': artist_rjson})

def get_users_top_songs(request):
    global global_token

    authToken = global_token
    headers = {
      'Authorization': 'Bearer '+authToken
    }

    print("HEADERS",headers)

    # get users top tracks frin the personalization endpoint

    url_tracks = ('https://api.spotify.com/v1/me/top/tracks?limit=5&time_range=short_term')
    print(url_tracks)

    response = requests.request("GET", url_tracks, headers=headers)

    rjson = response.json()

    return render(request, 'myapp/songs.html', {'searchResults': rjson})

# extracts your top 50 songs to view, and then you click button and it calls export_playlist function
def extract_playlist(request):
    global global_token

    authToken = global_token
    headers = {
      'Authorization': 'Bearer '+authToken
    }

    # get users top tracks frin the personalization endpoint

    url_tracks = ('https://api.spotify.com/v1/me/top/tracks?limit=50&time_range=short_term')
    print(url_tracks)

    response = requests.request("GET", url_tracks, headers=headers)

    rjson = response.json()

    return render(request, 'myapp/extractPlaylist.html', {'searchResults': rjson})
