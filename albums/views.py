from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Album, ArtistLabel, Band
from .forms import ReviewForm


class AlbumView(ListView):

    model = Album
    queryset = Album.objects.filter(draft=False)


class AlbumDetailView(DetailView):

    model = Album
    slug_field = 'url'


class ArtistDetailView(View):

    def get(self, request, slug):
        artist = ArtistLabel.objects.get(url=slug)
        context = {
            'artist': artist,
        }
        return render(request, 'artist_detail.html', context)


class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        album = Album.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.album = album
            form.save()
        return redirect(album.get_absolute_url())
