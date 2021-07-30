from django.urls import path

from . import views


urlpatterns = [
    path('', views.AlbumView.as_view(), name='index'),
    path('<slug:slug>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('review/<int:pk>/', views.AddReview.as_view(), name='add_review'),
]

