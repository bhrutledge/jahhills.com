from django.contrib import admin

from .models import Release, Song, Video, Press


class ReleaseAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ('title', 'slug', 'date', 'cover_url', 'player_code',
              'description', 'credits', 'publish', 'publish_on', 'priority',)
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'date', 'publish', 'publish_on', 'priority',)

admin.site.register(Release, ReleaseAdmin)


class SongAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ('title', 'slug', 'release', 'track', 'player_code',
              'description', 'credits', 'lyrics', 'publish', 'publish_on',)
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'release', 'track', 'publish', 'publish_on',)

admin.site.register(Song, SongAdmin)


class VideoAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ('title', 'slug', 'source_url', 'embed_code', 'preview_url',
              'release', 'description', 'credits', 'publish', 'publish_on',)
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'source_url', 'release', 'publish', 'publish_on',)

admin.site.register(Video, VideoAdmin)


class PressAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ('title', 'date', 'source_url', 'body', 'quote', 'release',
              'publish', 'publish_on',)
    list_display = ('title', 'date', 'release', 'publish', 'publish_on',)

admin.site.register(Press, PressAdmin)
