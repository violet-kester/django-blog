from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # set columns to be displayed
    list_display = ['title', 'slug', 'author', 'publish', 'status']

