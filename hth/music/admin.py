from django.contrib import admin

from .models import Release, Song, Video


class ReleaseAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'date', 'cover_url', 'description', 'credits',
              'publish', 'publish_on',)
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'date', 'publish', 'publish_on',)

admin.site.register(Release, ReleaseAdmin)


class SongAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'release', 'track', 'description', 'credits',
              'lyrics', 'publish', 'publish_on',)
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'release', 'track', 'publish', 'publish_on',)

admin.site.register(Song, SongAdmin)


class VideoAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'source_url', 'embed_code', 'preview_url',
              'release', 'description', 'credits', 'publish', 'publish_on',)
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'release', 'publish', 'publish_on',)

admin.site.register(Video, VideoAdmin)
