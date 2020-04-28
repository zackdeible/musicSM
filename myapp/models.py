from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Track(models.Model):
    track_name = models.CharField(max_length=500)
    album_name = models.CharField(max_length=500)
    artist_name = models.CharField(max_length=500)
    album_pic = models.CharField(max_length=500)
    our_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    spotify_url = models.CharField(max_length=500, default=None)
    apple_url = models.CharField(max_length=500, default=None)

    def __str__(self):
        return self.track_name

class Playlist(models.Model):
    playlist_name = models.CharField(max_length=500)
    tracks = models.ManyToManyField(Track, default=None)
    users = models.ManyToManyField(User, blank=True, default=None)

    def __str__(self):
        return self.playlist_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    target = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='targets', on_delete=models.CASCADE)
    playlists = models.ManyToManyField(Playlist, default=None)

    def __str__(self):
        return self.user.username
