from django.contrib import admin
from .models import Post, Gig, Release


class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'body', 'publish', 'publish_on')
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'publish', 'publish_on')

admin.site.register(Post, PostAdmin)


class GigAdmin(admin.ModelAdmin):
    fields = ('date', 'slug', 'venue', 'city','description', 'details',
              'publish', 'publish_on')
    prepopulated_fields = {'slug': ('date',)}
    list_display = ('date', 'venue', 'city')

admin.site.register(Gig, GigAdmin)


class ReleaseAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'date', 'description', 'credits',
              'publish', 'publish_on')
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'date', 'publish', 'publish_on')

admin.site.register(Release, ReleaseAdmin)

