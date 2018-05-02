from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class playlists(models.Model):
    userdetails = models.ForeignKey(User,on_delete=models.DO_NOTHING,)
    playlistname = models.CharField(max_length=200)
    albumart = models.CharField(max_length=200)
    playlisttype = models.CharField(max_length=200,default = "CREATED")
    ts = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.playlistname 

class playlistsongs(models.Model):
    userdetails = models.ForeignKey(User,on_delete=models.DO_NOTHING,)
    playlist = models.ForeignKey(playlists)
    url = models.CharField(max_length=200)
    albumart = models.CharField(max_length=200)
    songname = models.CharField(max_length=200)
    videoid = models.CharField(max_length=200)


