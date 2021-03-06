from django.shortcuts import render
import argparse
from .models import playlists,playlistsongs
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

DEVELOPER_KEY = 'AIzaSyDDMS-QHJhvX3_zjnQK4yFb6rxvtabfNw0'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Create your views here.
@login_required(login_url="/login/")
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

@login_required(login_url="/login/")
def playinbuiltplaylist(request,offset):
    return render(request,'playinbuilt.html',{"playlistid":offset})


@login_required(login_url="/login/")
def youtubesearch(request):
    if request.method == "POST":
        query = request.POST.get('q')
        print request.user
        try:
            searchRes = youtube_search(query,10)
            print searchRes
            print searchRes['items'][0]
            return render(request,'searchresults.html',{"results":searchRes['items'],"query":query})
        except HttpError, e:
            print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)
    
    return render(request,'searchresults.html',{"message":True})

@login_required(login_url="/login/")
def ytplayer(request,offset):
    return render(request,'ytplayer.html',{"videoId":offset})

@login_required(login_url="/login/")
def playlists_view(request):
    errormessage = ''
    if request.method == "POST":
        playlistName = request.POST.get("playlistname")
        albumArt = request.POST.get("albumart")

        if not playlistName:
            errormessage = "having a playlist name is compulsary"
        else:
            if not albumArt:
                albumArt = "https://yt3.ggpht.com/pHwZj3tkgC3SJFbuqebBoT7WtVcIwAijEmcbe9VDCauv9ZlG6uS2zjvZQUSO7SfFqa3xjYqGp_L4QbM7=s900-mo-c-c0xffffffff-rj-k-no"
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
    sharedsongdata = ''
    i = 0
    for data in sharedplaylist:
        closed =False
        if(i%4 == 0 ):
           sharedsongdata = sharedsongdata + '<div class = "row">'
        sharedsongdata  = sharedsongdata +'<div class = "col-md-3 ">' + '<a href = "/insideplaylist/'+ str(data.id) +'"> <figure> <img height="250" width="250" class="albumart" src="'+data.albumart+'" alt= "albumart"><figcaption><h3>' + data.playlistname + '</h3></figcaption></figure></a></div>'
        if(i%4 == 3 ):
            sharedsongdata = sharedsongdata + '</div><br>'
            closed = True
        i = i+1
    if sharedsongdata != '' and  not closed:
        sharedsongdata = sharedsongdata + '</div><br>'
    
    return render(request,'viewplaylists.html',{"ownplaylists":ownsongdata, "sharedplaylists": sharedsongdata, "errormessage":errormessage})

@login_required(login_url="/login/")
def showplaylistcontent(request,offset):
    sharedmessage = ''
    songerror = ''
    results = ''
    print request.method
    if request.method == 'POST' and 'albumart' in request.POST:
        print "heranfkmgasvkm"
        videoId = request.POST.get('videoid')
        albumArt = request.POST.get('albumart')
        title = request.POST.get('title')
        playlistid = request.POST.get('playlistid')
        songaddto = playlists.objects.get(id = playlistid)
        position = playlistsongs.objects.filter(userdetails=request.user, playlist = playlistid).count()
        newEnty = playlistsongs(userdetails = request.user, playlist = songaddto, albumart = albumArt, songname = title ,videoid = videoId,position=position)
        newEnty.save()

        

    if request.method == 'POST' and 'newsong' in request.POST:
        newsong = request.POST.get("newsong")
        try:
            songaddto = playlists.objects.get(id = offset)
            searchsong = youtube_search(newsong,5)
            results = searchsong['items']
            print searchsong['items'][0]['id']['videoId']
            #newEnty = playlistsongs(userdetails = request.user, playlist = songaddto, url = newsong, albumart = searchsong['items'][0]['snippet']['thumbnails']['high']['url'], songname = searchsong['items'][0]['snippet']['title'] ,videoid = searchsong['items'][0]['id']['videoId'])
            #newEnty.save()
        except:
            songerror = 'Song not found on url does not exist'
    
    if request.method == 'POST' and 'shareduser' in request.POST:
        shareduser = request.POST.get('shareduser')
        try:
            shareduserobj = User.objects.get(username = shareduser)
            sharedplaylist = playlists.objects.get(id = offset)
            newEnty = playlists(userdetails = request.user, playlistname = sharedplaylist.playlistname, albumart = sharedplaylist.albumart, playlisttype = 'SHARED')
            newEnty.save()
        except:
            sharedmessage = 'Username does not exist!!'
            
    print sharedmessage
    selectedplaylist = playlists.objects.get(id = offset)    
    songs = playlistsongs.objects.filter(userdetails = request.user, playlist = selectedplaylist)


    return render(request,"showplaylistcontent.html", {"songs": songs, "playlistid":offset,"sharedmessage":sharedmessage, "songerror": songerror,"results" : results} )

@login_required(login_url="/login/")
def playaplaylist(request,offset):
    
    offsetdata = offset.split('/')
    playlist = playlists.objects.get(id = offsetdata[0])
    songs = playlistsongs.objects.filter(userdetails = request.user, playlist = playlist)
    print songs
    if(offsetdata[1]=='shuffle=true'):
        songs = songs.order_by('?')

    videoId = ''
    firstvid = ''
    vidcount = 0
    for song in songs:
        if vidcount == 0:
            firstvid = song.videoid
        else:
            videoId = videoId + song.videoid + ','
        vidcount = 1
    print videoId
    return render(request,"playlistplayer.html", {"songs": songs, "videoId":videoId, "firstvid":firstvid} )

def deletesong(request,offset):

    instance = playlistsongs.objects.get(id=offset.split('/')[1]).delete()
    #instance.save()
    return HttpResponseRedirect('/insideplaylist/'+offset.split('/')[0])


@csrf_exempt
def songsort(request):
    value = request.POST.get('value')
    print value
    value = json.loads(value)
    print type(value)
    for key, val in value.iteritems():
        print str(key)+ ":" + str(val)
        playlistsongs.objects.filter(pk=key).update(position=val)
        print "updated"

    
    #for pk, position in self.request_json.items():
     #   playlistsongs.objects.filter(pk=pk).update(position=position)
    return JsonResponse({'saved': 'OK'})