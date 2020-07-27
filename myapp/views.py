from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import path
import urllib.parse
from .models import Playlist, Track, Profile
import requests, json
import datetime
import jwt

from django.conf import settings

#######################################################
#------------------ Apple Music API-------------------#
#######################################################
def getValidAppleToken():
    secret = """-----BEGIN PRIVATE KEY-----
MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgs8ZhcQHRGdo8lqaPUngLm/CGNnStUQFodIbYu6tMdB+gCgYIKoZIzj0DAQehRANCAAQ5eK421dcRn262EEXMQRs4M/MqGJSSa/WpSWJVkVc9CWNxjAtXYubgH8TmBKDpD+kxp8Hvs960DXS/GJ4p3Wrv
-----END PRIVATE KEY-----"""
    teamId = "3GNG4X7MEN"
    keyId = "9M495JYKHU"
    alg = 'ES256'

    time_now = datetime.datetime.now()
    time_expired = datetime.datetime.now() + datetime.timedelta(hours=12)

    headers = {
        "alg": alg,
        "kid": keyId
        }

    payload = {
        "iss": teamId,
        "exp": int(time_expired.timestamp()),
        "iat": int(time_now.timestamp())
    }
    token = jwt.encode(payload, secret, algorithm=alg, headers=headers)
    token_str = token.decode('utf-8')
    return token_str

def apple_user_top_music(request):
    devToken = getValidAppleToken()
    token = request.GET.get('userToken')
    print(token)
    headers1 = {
      'Authorization': 'Bearer '+devToken,
      'Music-User-Token': ''+token
    }

    print("HEADERS",headers1)

    # get users top tracks frin the personalization endpoint

    url_tracks = ('https://api.music.apple.com/v1/me/recent/played')
    print(url_tracks)


    response = requests.request("GET", url_tracks, headers=headers1)

    print("------------", response)

    print("REQUEST", response.json())

    return render(request, 'myapp/appleUserTopMusic.html', {'data': response.json()})

def apple_music_auth(request):
    #secret = """
    #-----BEGIN PRIVATE KEY-----
    #MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgs8ZhcQHRGdo8lqaPUngLm/CGNnStUQFodIbYu6tMdB+gCgYIKoZIzj0DAQehRANCAAQ5eK421dcRn262EEXMQRs4M/MqGJSSa/WpSWJVkVc9CWNxjAtXYubgH8TmBKDpD+kxp8Hvs960DXS/GJ4p3Wrv
    #-----END PRIVATE KEY-----"""
    #secret = "https://api.music.apple.com/v1/catalog/us/songs/203709340"
    #secret = '-----BEGIN PUBLIC KEY-----\n' + 'MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgs8ZhcQHRGdo8lqaPUngLm/CGNnStUQFodIbYu6tMdB+gCgYIKoZIzj0DAQehRANCAAQ5eK421dcRn262EEXMQRs4M/MqGJSSa/WpSWJVkVc9CWNxjAtXYubgH8TmBKDpD+kxp8Hvs960DXS/GJ4p3Wrv' + '\n-----END PUBLIC KEY-----'
    #secret = '-----BEGIN PUBLIC KEY-----MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgs8ZhcQHRGdo8lqaPUngLm/CGNnStUQFodIbYu6tMdB+gCgYIKoZIzj0DAQehRANCAAQ5eK421dcRn262EEXMQRs4M/MqGJSSa/WpSWJVkVc9CWNxjAtXYubgH8TmBKDpD+kxp8Hvs960DXS/GJ4p3Wrv-----END PUBLIC KEY-----'
    #secret = '3GNG4X7MEN.music.com.musicSM'



    token_str = getValidAppleToken()

    headers1 = {
      'Authorization': 'Bearer '+token_str
    }

    print("HEADERS",headers1)

    # get users top tracks frin the personalization endpoint

    url_tracks = ('https://api.music.apple.com/v1/catalog/us/artists/178834')
    print(url_tracks)

    response = requests.request("GET", url_tracks, headers=headers1)
    print(response.json())
    #rjson = response.json()
    #print(rjson)



    return render(request, 'myapp/appleMusicAuth.html', {'token': token_str})



#######################################################
#------------------ Python Authentication-------------------#
#######################################################

def getValidToken(authCode):


    url = "https://accounts.spotify.com/api/token"

    if settings.STAGE == 'development':
        redirect_uri = urllib.parse.quote_plus(settings.DEVELOPMENT_AUTH_REDIRECT)
    elif settings.STAGE == 'production':
        # CHANGE BEFORE PUSHING
        redirect_uri = urllib.parse.quote_plus(settings.PRODUCTION_AUTH_REDIRECT)

    payload = ('grant_type=authorization_code&code='+
                authCode +
                '&redirect_uri='+redirect_uri)
    headers = {
      'Authorization': 'Basic YTk5Njg1ZjgzNWQyNDBjYjg3OTE1OGYyMTgzYmEwMDA6ODJkZmNjMzVkN2MxNGNhNzlhOGJjOGIyN2YwYmMzMzA=',
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data = payload)

    token = response.json()['access_token']
    print("---------------------",token)
    return token

# Create your views here.
def home(request):
    # Get the token code in the url
    ## TODO: make this not horrible

    authCode = request.GET.get('code')

    if authCode != None:
        print("AUTHCODE", authCode)
        token = getValidToken(authCode)
        if request.method == 'GET':
            #return redirect('user-top-music',token=token)
            #return redirect('/userTopMusic?token='+token)#render(request, 'myapp/userTopMusic.html')
            short_term = 'medium_term'
            data = get_top_songs(token, 5, short_term)

            return render(request, 'myapp/userTopMusic.html', {'searchResults': data, 'token': token})

    else:
        return render(request, 'myapp/musicServiceAuth.html')

def authRedirect(request):
    scope = str('user-top-read playlist-modify-public')
    redirectUrl = ''
    if settings.STAGE == 'development':
        redirectUrl = urllib.parse.quote_plus(settings.DEVELOPMENT_AUTH_REDIRECT)
    elif settings.STAGE == 'production':
        # CHANGE BEFORE PUSHING
        redirectUrl = urllib.parse.quote_plus(settings.PRODUCTION_AUTH_REDIRECT)

    clientId = settings.SOCIAL_AUTH_SPOTIFY_KEY
    print(redirectUrl, "------------------------")
    redirectFullUrl = 'https://accounts.spotify.com/en/authorize?client_id='+clientId+'&redirect_uri='+redirectUrl+'&response_type=code&scope='+scope
    print(redirectFullUrl)
    return redirect(redirectFullUrl)

def musicServiceAuth(request):
     return render(request, 'myapp/musicServiceAuth.html')

#######################################################
#------------------End Authentication-------------------#
#######################################################


#######################################################
#------------------Not currently used -------------------#
#######################################################

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

# I dont think this is used
def get_users_top_music(request):
    print('GET',request.GET)
    token = request.GET.get('token')

    print('TOKEN',token)

    headers = {
      'Authorization': 'Bearer '+token
    }

    print("HEADERS",headers)

    # get users top tracks frin the personalization endpoint

    url_tracks = ('https://api.spotify.com/v1/me/top/tracks?limit=5&time_range=medium_term')
    print(url_tracks)

    response = requests.request("GET", url_tracks, headers=headers)

    rjson = response.json()

    url_artists = ('https://api.spotify.com/v1/me/top/artists?limit=5&time_range=medium_term')
    print(url_artists)

    response1 = requests.request("GET", url_artists, headers=headers)

    artist_rjson = response1.json()

    return render(request, 'myapp/userTopMusic.html', {'searchResults': rjson, 'artists': artist_rjson, 'token': token})


#######################################################
#------------------END Not currently used -------------------#
#######################################################


#######################################################
#------------------Currently In Production-------------------#
#######################################################

# Calls spotify API for userprofile, calls spotify api to get top 50 songs, calls spotify API to add songs to playlist that we just made
def export_playlist(request):

    # 1) get auth TOKEN
    # 2) get userprofile of current user
    # 3) create (POST) playlist with: https://api.spotify.com/v1/users/{user_id}/playlists
    # 3.1) look up all the songs of that playlist name, get the spotify ids in a list format
    # 4) add tracks to that playlist with: https://api.spotify.com/v1/playlists/{playlist_id}/tracks


    print("-----------------", request.POST)

    token = request.POST.get('token')

    #print("WE MADE IT HERE BBY")
    if request.method=='POST':
        playlist_name = request.POST.get("playlist-name")

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


    url = "https://api.spotify.com/v1/users/"+user_id+"/playlists"

    payload = "{\n    \"name\": \""+playlist_name+"\"\n}"
    headers = {
    'content-type': 'application/json',
    'Authorization': 'Bearer '+authToken,

    }

    create_playlist = requests.request("POST", url, headers=headers, data = payload)

    #print(create_playlist.text.encode('utf8'))

    playlist_id_json = create_playlist.json()
    playlist_id = playlist_id_json['id']


    ######## get songs to add to playlists
    top_song_dict = get_top_songs(authToken, 50, 'medium_term')

    print("--------",top_song_dict['items'][1]['uri'])

    top_song_data = top_song_dict['items']
    playlist_uris_list = ''

    for song in top_song_data:
        #print(song['uri
        song_string = str(song['uri'])
        playlist_uris_list = playlist_uris_list+song_string+"\", \""

    # This is weird but need to format it for the API call and this jenky ass way deletes the extra "" at the end
    new_set = playlist_uris_list[:-4]

    #print(str(playlist_uris_list))

    data_formatted = "{\n    \"uris\": [\""+new_set+"\"]\n}"

    # add songs to the playlist

    url_add = 'https://api.spotify.com/v1/playlists/'+playlist_id+'/tracks'
    add_songs = requests.request("POST", url_add, headers=headers, data=data_formatted)


    return render(request, 'myapp/exportPlaylist.html', {'searchResults': top_song_dict})





# Render top artist page and get top artists -> need to make helper function
def get_users_top_artists(request):

    authToken = request.POST.get('token')

    print("--------------", authToken)
    headers = {
      'Authorization': 'Bearer '+authToken
    }

    url_artists = ('https://api.spotify.com/v1/me/top/artists?limit=5&time_range=medium_term')


    response1 = requests.request("GET", url_artists, headers=headers)

    artist_rjson = response1.json()
    print("ARTISTS", artist_rjson)

    return render(request, 'myapp/topArtists.html', {'artists': artist_rjson, 'token': authToken})

# render top songs
def get_users_top_songs(request):
    token = request.POST.get('token')

    data = get_top_songs(token, 5, 'medium_term')


    return render(request, 'myapp/songs.html', {'searchResults': data, 'token': token})



# extracts your top 50 songs to view, and then you click button and it calls export_playlist function
# I think just used in rendering right now
def extract_playlist(request):
    authToken = request.POST.get('token')
    print(authToken)
    headers = {
      'Authorization': 'Bearer '+authToken
    }

    # get users top tracks from the personalization endpoint

    url_tracks = ('https://api.spotify.com/v1/me/top/tracks?limit=50&time_range=medium_term')
    print(url_tracks)

    response = requests.request("GET", url_tracks, headers=headers)

    rjson = response.json()

    return render(request, 'myapp/extractPlaylist.html', {'searchResults': rjson, 'token':authToken})



#######################################################
#------------------Helper Functions-------------------#
#######################################################

# Get amount of top songs (could add artists/tracks paramter too)
def get_top_songs(authToken, amount, time_range):

    # Authorization
    headers = {
      'Authorization': 'Bearer '+authToken
    }

    amount = str(amount)

    # Call api, could add another param of type (artists or tracks)

    url_tracks = ('https://api.spotify.com/v1/me/top/tracks?limit='+amount+'&time_range='+time_range)
    response = requests.request("GET", url_tracks, headers=headers)
    rjson = response.json()
    return rjson
