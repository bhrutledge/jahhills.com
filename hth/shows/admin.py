from django.contrib import admin
from .models import Gig


class GigAdmin(admin.ModelAdmin):
    fields = ('date', 'slug', 'venue', 'city','description', 'details',
              'publish', 'publish_on',)
    prepopulated_fields = {'slug': ('date',)}
    list_display = ('date', 'venue', 'city',)

admin.site.register(Gig, GigAdmin)

