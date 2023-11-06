from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    """ A sitemap for the Post model."""

    # how often the content on a page is expected to change
    changefreq = 'weekly'

    # the relative priority of a page within the website
    priority = 0.9

    # returns a queryset of all published posts
    def items(self):
        return Post.objects.filter(status='PB')

    # returns the last modified date of a post object
    def lastmod(self, obj):
        return obj.updated
