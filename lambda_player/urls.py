"""lambda_player URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from users.views import home,youtubesearch,ytplayer,playlists_view,showplaylistcontent,playaplaylist,playinbuiltplaylist,deletesong,songsort
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, name='login',kwargs={'redirect_authenticated_user': True}),
    url(r'^logout/$', auth_views.logout,{'next_page': '/login/'}),
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
    
    url(r'^youtubesearch$', youtubesearch),
    url(r'^playback/(.*)$', ytplayer),
    url(r'^deletesong/(.*)$', deletesong),
    url(r'^play/(.*)$', playaplaylist),
    url(r'^playinbuilt/(.*)$', playinbuiltplaylist),
    url(r'^songsorting/$',songsort,name='song_sorting'),
    url(r'^playlists/$', playlists_view),
    url(r'^insideplaylist/(.*)$', showplaylistcontent),

    url(r'^', home),
]
