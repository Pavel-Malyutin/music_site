from django.urls import path

from . import views


urlpatterns = [
    path('', views.AlbumView.as_view(), name='index'),
    path('filter/', views.FilterAlbumsView.as_view(), name='filter'),
    path('<slug:slug>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('review/<int:pk>/', views.AddReview.as_view(), name='add_review'),
    path('artist/<str:slug>/', views.ArtistView.as_view(), name='artist_detail'),
    path('band/<str:slug>/', views.BandView.as_view(), name='band_detail'),
]

