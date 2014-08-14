from django.contrib import admin

from .models import Release


class ReleaseAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'date', 'description', 'credits',
              'publish', 'publish_on',)
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'date', 'publish', 'publish_on',)

admin.site.register(Release, ReleaseAdmin)

