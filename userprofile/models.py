from django.db import models
from django_countries.fields import CountryField
from datetime import datetime
from .utils import CountryName
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()


def get_filename(self, filename):
    """ Generates a custom filename for uploads based on author's username and the post's creation date """

    extension = filename.split('.')[-1]
    t = datetime.now()
    datetime_str = f"{t.year}-{t.month}-{t.day}-{t.hour}{t.minute}{t.second}"

    return f"uploads/profiles/{self.user.username}_{datetime_str}.{extension}"


class Follower(models.Model):
    """
    This is an intermediary model for handling the relationship between users and followers. It allows us to store
    additional information that a ManyToMany field won't capture on its own like when the relationship was created.
    This code is adapted from 'Django 3 By Example' by Antonio Mele.
    """

    user_from = models.ForeignKey(
        'userprofile.Profile', related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(
        'userprofile.Profile', related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.user_from.user.username} follows {self.user_to.user.username}"


class Profile(models.Model):
    user = models.OneToOneField(
        USER_MODEL, null=True, on_delete=models.CASCADE)

    blog_title = models.CharField(blank=True, null=True, max_length=255,
                                  help_text='Add a blog title or headline to go beneath your name')

    bio = models.TextField(blank=True, null=True)

    profile_picture = models.ImageField(
        blank=True, null=True, upload_to=get_filename)

    cover_photo = models.ImageField(
        blank=True, null=True, upload_to=get_filename)

    city = models.CharField(blank=True, null=True, max_length=100)

    country = CountryField(
        blank_label='(select country)', blank=True, null=True)

    website = models.URLField(
        help_text='You can add a link to your personal website', blank=True, null=True)

    twitter = models.CharField(max_length=16, blank=True, null=True)

    github = models.CharField(max_length=100, blank=True, null=True)

    following = models.ManyToManyField(
        'self', through=Follower, related_name='followers', symmetrical=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.username}) | {self.user.email}"

    def get_location(self):
        """ Returns a string with the user's location based on their chosen city/country. """
        if not self.city and not self.country:
            return

        if self.country.name:
            country = CountryName.get_country_name(self.country.name)
            if self.city:
                return f"{self.city}, {country}"
            else:
                return f"{country}"
        else:
            return f"{self.city}"
