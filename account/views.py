from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth import authenticate, login, logout
from myapp.models import Playlist, Track, Profile, Post, Album, Artist
from django.contrib.auth.models import User
import requests, json
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

# Create your views here.
def home(request):
    # pass in the user data for followers and following by counting how many people are in it
    # how to get data from db example: data = Playlist.objects.filter(users=current_user)
    print("-----",request.session)
    cur_user = request.user
    request.session['test'] = "work"
    print("IS THIS REAL RN IS THIS REAL", request.session.get('spotify_token'))

    # filter to see if there is already a profile
    profile_exists = Profile.objects.filter(user=cur_user)
    if profile_exists.exists():
        print("exists")
    else:
        u = Profile(user=cur_user)
        u.save()

    # get profile
    profile = Profile.objects.get(user=cur_user)
    follower_count = profile.follower.all().count()
    following_count = profile.following.all().count()

    description = profile.description
    if description == '':
        description = "Edit profile to add a description"

    posts = Post.objects.all().filter(user_id=cur_user)


    data = {
        'follower': follower_count,
        'following': following_count,
        'description': description,
        'name': cur_user,
        'profile': profile,
        'posts': posts
    }
    return render(request, 'account/home.html', {'data': data})


def login_view(request):

    return render(request, 'account/login.html', {})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('home')

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        print(request.POST['psw'])
        print("form", form)
        username = form.cleaned_data.get('username')
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            print("FUCL YES")
            return redirect('home')

        #if form.is_valid():
            #print("valid")
            #username = form.cleaned_data.get('username')
            #password = form.cleaned_data.get('password')
            #print("username--------", username)
            #user = authenticate(username=username, password=password)
            #print("user", user)

    print(request.POST)

    print('MADE IT HERE')
    return render(request, 'account/login.html', {})

def register(request):
    print("Im here 1")
    if request.method == 'POST':
        print("Im here")
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("-------", form.cleaned_data)
            email = form.cleaned_data.get('email')


            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})



def get_users(request):
    cur_user = request.user
    cur_user_id = cur_user.id
    users = Profile.objects.all().exclude(user = cur_user_id)

    return render(request, 'account/users.html', {'users': users, 'cur_user': cur_user})

def follow(request):
    print(request.POST)
    cur_user = request.user

    if request.method == 'POST':
        # get the user that we want to follow
        username = request.POST['username']

        # get the user we want to follows user table and profile
        follow_user = User.objects.get(username=username)
        follow_profile = Profile.objects.get(user=follow_user.id)

        # get the current users profile
        cur_profile = Profile.objects.get(user=cur_user.id)

        # add to following and follower to both profiles
        cur_profile.following.add(follow_user.id)
        follow_profile.follower.add(cur_user.id)
        return redirect('home')


    return render(request, 'account/users.html')

def unfollow(request):
    cur_user = request.user

    if request.method == 'POST':
        username = request.POST['username']

        # get user we want to unfollow user table and profile
        unfollow_user = User.objects.get(username=username)
        unfollow_profile = Profile.objects.get(user=unfollow_user.id)

        # get the current users profile
        cur_profile = Profile.objects.get(user=cur_user.id)

        # delete from following and follower to both profiles
        cur_profile.following.remove(unfollow_user.id)
        unfollow_profile.follower.remove(cur_user.id)
        return redirect('home')



    return render(request, 'account/users.html')

# renders the edit_profile page, so far it can only change description with the change description file
def edit_profile(request):
    return render(request, 'account/editProfile.html')

# changes the description for a user
def change_description(request):
    cur_user_id = request.user.id
    if request.method == 'POST':
        new_description = request.POST['description']
        cur_profile = Profile.objects.get(user=cur_user_id)
        cur_profile.description = new_description
        cur_profile.save()
        redirect('home')

    return redirect('home')


def create_post(request):
    try:
        embed_link = iFrame_generate(request.POST['url'])
        return render(request, 'account/createPost.html', {'link': embed_link})
    except:
        return render(request, 'account/createPost.html')

def save_post(request):
    cur_user = request.user
    if request.method =='POST':
        subject = request.POST['subject']
        content = request.POST['content']
        new_post = Post(user_id=cur_user, subject=subject, content=content)
        new_post.save()
        redirect('home')

    return redirect('home')

# display the feed
def feed(request):
    print(request.session.get("test"))

    cur_user = request.user
    profile = Profile.objects.get(user=cur_user)
    following = profile.following.all()
    print(following)

    feed = []
    for follow in following:
        potential_feed = Post.objects.all().filter(user_id=follow)
        # do not want empty feed if a user didnt post
        if potential_feed.exists():
            feed.append(potential_feed)

    print(feed)


    return render(request, 'account/feed.html', {'feed': feed})


# get the top songs for a user generated by Spotify
def generate_top_songs(request):

    token = request.session.get('spotify_token')

    # url_tracks = ('https://api.spotify.com/v1/me/top/tracks?limit=5&time_range=medium_term')
    #
    # headers = {
    #   'Authorization': 'Bearer '+token
    # }
    #
    #
    # print("ayy", token)
    amount = 50
    time_range = 'medium_term'

    top_artists = spotify_get_top(token, 'artists', amount, time_range)
    top_tracks = spotify_get_top(token, 'tracks', amount, time_range)
    
    data = {
        'top_artists': top_artists,
        'top_tracks': top_tracks
    }
    return render(request, 'account/generateTopSongs.html', {'data': data})


def search_songs(request):

    # cur_user = request.user
    #
    #
    # # filter to see if there is already a profile
    # playlist_exists = Playlist.objects.filter(playlist_name="Default", users=cur_user)
    # if playlist_exists.exists():
    #     print("exists")
    # else:
    #     p = Playlist(playlist_name="Default", users=cur_user)
    #     p.save()
    #
    #
    # playlist = Playlist.objects.get(playlist_name="Default", users=cur_user)

    #return render(request, 'account/users.html', {})



    return render(request, 'account/searchSongs.html')

def search(request):
    token = request.session.get('spotify_token')


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
                token)

        print(url, "------------")
        print(request.GET)
        response = requests.request("GET", url)

        print(response)

        rjson = response.json()
        return render(request, 'account/searchResults.html', {'searchResults': rjson})
    return render(request, 'account/searchResults.html')

    #return render(request, '/search.html', {'searchResults':rjson, 'playlists': playlist})

def view_profile(request):
    # how to get data from db example: data = Playlist.objects.filter(users=current_user)

    cur_user = request.user


    v_user = request.POST['v_user']

    v_username = User.objects.get(username=v_user)
    profile = Profile.objects.get(user=v_username.id)

    follower_count = profile.follower.all().count()
    following_count = profile.following.all().count()

    description = profile.description
    if description == '':
        description = "These dumbasses dont have a description"

    posts = Post.objects.all().filter(user_id=v_username.id)


    data = {
        'follower': follower_count,
        'following': following_count,
        'description': description,
        'name': v_user,
        'profile': profile,
        'posts': posts
    }
    return render(request, 'account/viewProfile.html', {'data': data})

############### ---------------- iFrame Function -------------- #############
def iFrame_generate(url):
    s = url.split("/")
    type = s[-2]
    code = s[-1]

    str = "https://open.spotify.com/embed/"+type+"/"+code
    return str



############### ---------------- Spotify Helper Functions -------------- #############
# Get amount of top songs (could add artists/tracks paramter too)
def spotify_get_top(token, type, amount, time_range):
    # Authorization
    headers = {
      'Authorization': 'Bearer '+token
    }
    amount = str(amount)

    # Call api, could add another param of type (artists or tracks)
    url_tracks = ('https://api.spotify.com/v1/me/top/'+type+'?limit='+amount+'&time_range='+time_range)
    response = requests.request("GET", url_tracks, headers=headers)
    rjson = response.json()
    return rjson
