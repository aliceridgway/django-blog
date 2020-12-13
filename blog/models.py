from django.db import models
import datetime
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings
from .helpers import get_post_slug
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField

def get_filename(self, filename):
    """ Generates a custom filename for uploads based on author's username and the post's creation date """

    extension = filename.split('.')[-1]
    t = self.created
    datetime_str = f"{t.year}-{t.month}-{t.day}-{t.hour}{t.minute}{t.second}"

    return f"uploads/{self.author.username}_{datetime_str}.{extension}"


class Post(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    title = models.CharField(max_length=255)
    feature_image = models.ImageField(blank=True, null=True, upload_to=get_filename, default='thePOST-default.jpg')
    body = RichTextField(blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique_with=['author__username'], always_update=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created = models.DateTimeField(default=timezone.now)
    published = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} | by {self.author.username}"
