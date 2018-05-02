from django.contrib import admin

# Register your models here.
from .models import playlists, playlistsongs

class playlistsadmin(admin.ModelAdmin):
    list_display=["userdetails","playlistname","albumart","playlisttype","ts"]

class playlistsongsadmin(admin.ModelAdmin):
    list_display=["userdetails","playlist","url",'albumart','songname','videoid']

admin.site.register(playlists,playlistsadmin)
admin.site.register(playlistsongs,playlistsongsadmin)