from django.contrib import admin

from .models import Venue, Gig


class VenueAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ('name', 'city', 'website')

admin.site.register(Venue, VenueAdmin)


class GigAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ('date', 'slug', 'venue', 'description', 'details',
              'publish', 'publish_on',)
    prepopulated_fields = {'slug': ('date',)}
    raw_id_fields = ('venue',)
    list_display = ('date', 'venue',)

admin.site.register(Gig, GigAdmin)
