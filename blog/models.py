from django.db import models
import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings
from .helpers import get_post_slug
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField

# Create your models here.
class Post(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    title = models.CharField(max_length=255)
    body = RichTextField(blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique_with=['author__username'], always_update=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created = models.DateTimeField(default=timezone.now)
    published = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} | by {self.author.username}"

    # def get_absolute_url(self):
    #     return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
