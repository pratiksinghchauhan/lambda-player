from django.shortcuts import render
import argparse
from .models import playlists,playlistsongs

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


def playinbuiltplaylist(request,offset):
    return render(request,'playinbuilt.html',{"playlistid":offset})



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
        ownsongdata  = ownsongdata +'<div class = "col-md-3 ">' + '<a href = "/insideplaylist/'+ str(data.id) +'"> <figure> <img height="250" width="250" class="albumart" src="'+data.albumart+'" alt= "albumart"><figcaption><h3>' + data.playlistname + '</h3></figcaption></figure></a></div>'
        if(i%4 == 3 ):
            ownsongdata = ownsongdata + '</div><br>'
            closed = True
        i = i+1
    if ownsongdata != '' and  not closed:
        ownsongdata = ownsongdata + '</div><br>'
    
    print ownsongdata

    sharedplaylist = playlists.objects.filter(userdetails = request.user, playlisttype = "SHARED")
  

    return render(request,'viewplaylists.html',{"ownplaylists":ownsongdata, "sharedplaylists": sharedplaylist})


def showplaylistcontent(request,offset):
    if request.method == 'POST' and 'newsong' in request.POST:
        newsong = request.POST.get("newsong")
        songaddto = playlists.objects.get(id = offset)
        searchsong = youtube_search(newsong,1)
        print searchsong['items'][0]['id']['videoId']

        newEnty = playlistsongs(userdetails = request.user, playlist = songaddto, url = newsong, albumart = searchsong['items'][0]['snippet']['thumbnails']['high']['url'], songname = searchsong['items'][0]['snippet']['title'] ,videoid = searchsong['items'][0]['id']['videoId'])
        newEnty.save()
    
    if request.method == 'POST' and 'shareduser' in request.POST:
        shareduser = request.POST.get('shareduser')
        shareduserobj = User.objects.get(username = shareduser)
        sharedplaylist = playlists.objects.get(id = offset)
        newEnty = playlists(userdetails = request.user, playlistname = sharedplaylist.playlistname, albumart = sharedplaylist.albumart, playlisttype = 'SHARED')
        newEnty.save()

    selectedplaylist = playlists.objects.get(id = offset)    
    songs = playlistsongs.objects.filter(userdetails = request.user, playlist = selectedplaylist)


    return render(request,"showplaylistcontent.html", {"songs": songs, "playlistid":offset} )

def playaplaylist(request,offset):
    playlist = playlists.objects.get(id = offset)
    songs = playlistsongs.objects.filter(userdetails = request.user, playlist = playlist)
    videoId = ''
    for song in songs:
        videoId = videoId + song.videoid + ','
    print videoId
    return render(request,"ytplayer.html", {"songs": songs, "videoId":videoId} )

