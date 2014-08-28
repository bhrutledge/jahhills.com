from django.contrib import admin

from .models import Venue, Gig


class VenueAdmin(admin.ModelAdmin):
    fields = ('name', 'city', 'website')

admin.site.register(Venue, VenueAdmin)


class GigAdmin(admin.ModelAdmin):
    fields = ('date', 'slug', 'venue', 'city','description', 'details',
              'publish', 'publish_on',)
    prepopulated_fields = {'slug': ('date',)}
    list_display = ('date', 'venue', 'city',)

admin.site.register(Gig, GigAdmin)
