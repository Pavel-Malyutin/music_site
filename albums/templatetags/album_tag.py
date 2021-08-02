from django import template
from albums.models import Band, Album


register = template.Library()


@register.simple_tag()
def get_bands():
    return Band.objects.all()


@register.inclusion_tag('albums/tags/last_albums.html')
def get_last_albums(count=3):
    albums = Album.objects.order_by('id')[:count]
    return {'last_albums': albums}
