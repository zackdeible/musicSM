from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Artist(models.Model):
    artist_name = models.CharField(max_length=500)
    artist_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    spotify_id = models.CharField(max_length=500, default=None)
    apple_id = models.CharField(max_length=500, default=None)

    def __str__(self):
        return self.artist_name

class Album(models.Model):
    album_name = models.CharField(max_length=500)
    album_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artist_id = models.ManyToManyField(Artist)
    spotify_id = models.CharField(max_length=500, default=None)
    apple_id = models.CharField(max_length=500, default=None)

    def __str__(self):
        return self.album_name



class Track(models.Model):
    track_name = models.CharField(max_length=500)
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE)
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE)
    track_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    spotify_id = models.CharField(max_length=500, default=None)
    apple_id = models.CharField(max_length=500, default=None)

    def __str__(self):
        return self.track_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    description = models.CharField(max_length=500)
    following = models.ManyToManyField(User, related_name="who_user_follows")
    follower = models.ManyToManyField(User, related_name="who_user_is_followed_by")

    def __str__(self):
        return self.user.username


class Playlist(models.Model):
    playlist_name = models.CharField(max_length=500)
    tracks = models.ManyToManyField(Track)
    users = models.ManyToManyField(User)
    playlist_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.playlist_name

class Post(models.Model):
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    # will turn into something that is a URI for playlist, track, album, artist
    subject = models.CharField(max_length=500)
    # post_date = models.Date and be the current date, want to make the other shit work first
