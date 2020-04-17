from django.contrib import admin
from .models import Track, Playlist, Profile

# Register your models here.
admin.site.register(Track)
admin.site.register(Playlist)
admin.site.register(Profile)
