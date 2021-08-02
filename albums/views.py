from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Album, ArtistLabel, Band, Genre
from .forms import ReviewForm


class GenreYear:

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Album.objects.filter(draft=False)


class AlbumView(GenreYear, ListView):
    model = Album
    queryset = Album.objects.filter(draft=False)


class AlbumDetailView(GenreYear, DetailView):
    model = Album
    slug_field = 'url'


class ArtistView(GenreYear, DetailView):
    model = ArtistLabel
    template_name = 'albums/artist.html'
    slug_field = 'name'


class BandView(DetailView):
    model = Band
    template_name = 'albums/band.html'
    slug_field = 'name'


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


class FilterAlbumsView(GenreYear, ListView):
    def get_queryset(self):
        queryset = Album.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres__in=self.request.GET.getlist('genre'))
        )
        return queryset
