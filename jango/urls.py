"""
URL configuration for jangosite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from website import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('about/', views.about),

    path('songs/', views.show_songs, name='show_songs'),
    path('songs/add', views.add_song, name='add_song'),
    path('songs/json', views.api_handler, name='api_handler'),
    path('songs/<int:song_id>', views.song_detail, name='song_details'),
    path('songs/clear', views.clear_songs, name='clear_songs'),
    path('fortune/', views.fortune, name='fortune'),
]

