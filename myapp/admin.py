from django.contrib import admin
from .models import Track, Playlist, Profile, Artist, Album, Post

# Register your models here.
admin.site.register(Track)
admin.site.register(Playlist)
admin.site.register(Profile)
admin.site.register(Album)
admin.site.register(Artist)
admin.site.register(Post)
