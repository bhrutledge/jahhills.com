from django.contrib import admin

from .models import Venue, Gig


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ('name', 'city', 'website', 'address', 'latitude', 'longitude')
    search_fields = ('name', 'city')


@admin.register(Gig)
class GigAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ('date', 'venue', 'description', 'details',
              'publish', 'publish_on',)
    raw_id_fields = ('venue',)

    date_hierarchy = 'date'
    list_display = ('date', 'venue', 'publish')
    search_fields = ('venue__name', 'venue__city')
