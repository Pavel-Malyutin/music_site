from django.urls import path

from . import views


urlpatterns = [
    path('', views.AlbumView.as_view(), name='index'),
    path('<slug:slug>/', views.AlbumDetailView.as_view(), name='album_detail'),
    # path('artist/<int:id>/', views.ArtistDetailView.as_view()), 'artist',
]

