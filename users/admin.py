from django.contrib import admin

# Register your models here.
from .models import playlists

class playlistsadmin(admin.ModelAdmin):
    list_display=["userdetails","playlistname","albumart","playlisttype","ts"]

admin.site.register(playlists,playlistsadmin)