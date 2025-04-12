# cms/models.py
from django.db import models
from django.utils import timezone


class News(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    url = models.URLField(unique=False)
    image_url = models.URLField(blank=True, null=True)
    pub_date = models.DateTimeField(default=timezone.now)
    source = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "News"
        ordering = ['-pub_date']

    def __str__(self):
        return self.title
