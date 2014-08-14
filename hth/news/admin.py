from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'body', 'publish', 'publish_on',)
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'publish', 'publish_on',)

admin.site.register(Post, PostAdmin)

