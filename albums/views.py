from django.shortcuts import render
from django.views.generic.base import View

from .models import Album, ArtistLabel


class AlbumView(View):

    def get(self, request):
        albums = Album.objects.all()

        context = {
            'albums': albums
        }
        return render(request, 'albums_list.html', context)


class AlbumDetailView(View):

    def get(self, request, slug):
        album = Album.objects.get(url=slug)
        context = {
            'album': album
        }
        return render(request, 'album_detail.html', context)


class ArtistDetailView(View):

    def get(self, request, id):
        artist = ArtistLabel.objects.get(id=id)

        context = {
            'artist': artist,
        }
        return render(request, 'artist_detail.html', context)
