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