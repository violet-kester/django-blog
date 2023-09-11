from django.db import models
from django.utils import timezone


class Post(models.Model):

    class Status(models.TextChoices):  # enum class
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    class Meta:
        # sort query results by publish date
        ordering = ['-publish']
        # index query results on ordering option for efficient retrieval
        indexes = [models.Index(fields=['-publish']), ]

    def __str__(self):
        return self.title