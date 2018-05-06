from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class playlists(models.Model):
    userdetails = models.ForeignKey(User,on_delete=models.DO_NOTHING,)
    playlistname = models.CharField(max_length=200)
    albumart = models.CharField(max_length=200,default="https://yt3.ggpht.com/pHwZj3tkgC3SJFbuqebBoT7WtVcIwAijEmcbe9VDCauv9ZlG6uS2zjvZQUSO7SfFqa3xjYqGp_L4QbM7=s900-mo-c-c0xffffffff-rj-k-no")
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
    position = models.IntegerField(default=0)
    class Meta:
        ordering = ['position', 'pk']


