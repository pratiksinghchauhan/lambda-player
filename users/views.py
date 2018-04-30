from django.shortcuts import render
import argparse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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

def ytplayer(request):
    return render(request,'ytplayer.html')

