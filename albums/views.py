from django.db.models import Q, Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Album, ArtistLabel, Band, Genre, Rating
from .forms import ReviewForm, RatingForm


class GenreYear:

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Album.objects.filter(draft=False)

    def get_country(self):
        return Album.objects.order_by().values('country').distinct()


class AlbumView(GenreYear, ListView):
    model = Album
    queryset = Album.objects.filter(draft=False).distinct()
    paginate_by = 6


class AlbumDetailView(GenreYear, DetailView):
    model = Album
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        return context


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
    paginate_by = 1

    def get_queryset(self):
        queryset = Album.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(country__in=self.request.GET.getlist('country')) |
            Q(genres__in=self.request.GET.getlist('genre'))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['year'] = ''.join([f"year={x}&" for x in self.request.GET.getlist('year')])
        context['country'] = ''.join([f"country={x}&" for x in self.request.GET.getlist('country')])
        context['genre'] = ''.join([f"genre={x}&" for x in self.request.GET.getlist('genre')])
        return context


class AddStarRating(View):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                album_id=int(request.POST.get('album')),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
