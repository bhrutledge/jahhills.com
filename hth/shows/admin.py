from django.contrib import admin
from django.db.models import Count

from .models import Venue, Gig


class GigInline(admin.TabularInline):
    model = Gig
    fields = ('date', 'description', 'publish_on')
    readonly_fields = ('date', 'description', 'publish_on')
    show_change_link = True
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ('name', 'city', 'website', 'address', 'latitude', 'longitude')
    inlines = [GigInline]
    search_fields = ('name', 'city')
    list_display = ('name', 'city', 'gigs')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(gigs=Count('gig'))

    def gigs(self, obj):
        return obj.gigs
    gigs.admin_order_field = 'gigs'


# TODO: Ad
@admin.register(Gig)
class GigAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = (
        'date', 'venue', 'description', 'details', 'publish', 'publish_on'
    )
    raw_id_fields = ('venue',)

    date_hierarchy = 'date'
    list_display = ('date', 'venue', 'publish')
    search_fields = ('venue__name', 'venue__city')
