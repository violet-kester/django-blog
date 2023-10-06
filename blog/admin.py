from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # set columns to be displayed
    list_display = ['id', 'title', 'slug', 'author', 'publish', 'status']

    # set column filters
    list_filter = ['status', 'created', 'publish', 'author']

    # set search fields
    search_fields = ['title', 'body']

    # prepopulate slug field based on title
    prepopulated_fields = {'slug': ('title',)}

    # use text input instead of dropdown menu for author field
    # helpful for large user bases
    raw_id_fields = ['author']

    # add date-based nav bar
    # useful for filtering posts by year, month, and day
    date_hierarchy = 'publish'

    # order columns by status and publish by default
    ordering = ['status', 'publish']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']