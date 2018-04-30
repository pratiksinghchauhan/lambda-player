from django.shortcuts import render
import argparse
from .models import playlists

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from django.contrib.auth.models import User


DEVELOPER_KEY = 'AIzaSyDDMS-QHJhvX3_zjnQK4yFb6rxvtabfNw0'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Create your views here.
def home(request):
    return render(request,'home.html')

def youtube_search(query,max_results):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=max_results
    ).execute()

    return search_response

    videos = []
    channels = []
    playlists = []



def youtubesearch(request):
    if request.method == "POST":
        query = request.POST.get('q')
        try:
            searchRes = youtube_search(query,10)
            print searchRes['items'][0]
            return render(request,'searchresults.html',{"results":searchRes['items'],"query":query})
        except HttpError, e:
            print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)

def ytplayer(request,offset):
    return render(request,'ytplayer.html',{"videoId":offset})

def playlists_view(request):
    if request.method == "POST":
        playlistName = request.POST.get("playlistname")
        albumArt = request.POST.get("albumart")

        print(request.user)
        newEnty = playlists(userdetails = request.user, playlistname = playlistName, albumart = albumArt)
        newEnty.save()
        
    
    ownplaylist = playlists.objects.filter(userdetails = request.user, playlisttype = "CREATED")
    print ownplaylist
    ownsongdata = ''
    i = 0
    for data in ownplaylist:
        closed =False
        if(i%4 == 0 ):
           ownsongdata = ownsongdata + '<div class = "row">'
        ownsongdata  = ownsongdata +'<div class = "col-md-3 ">' + '<figure> <img class="albumart" src="'+data.albumart+'" alt= "albumart"><figcaption><h3>' + data.playlistname + '</h3></figcaption></figure></div>'
        if(i%4 == 3 ):
            ownsongdata = ownsongdata + '</div><br>'
            closed = True
        i = i+1
    if ownsongdata != '' and  not closed:
        ownsongdata = ownsongdata + '</div><br>'
    
    print ownsongdata

    sharedplaylist = playlists.objects.filter(userdetails = request.user, playlisttype = "SHARED")
  

    return render(request,'viewplaylists.html',{"ownplaylists":ownsongdata, "sharedplaylists": sharedplaylist})


