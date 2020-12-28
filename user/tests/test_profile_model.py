from django.test import TestCase
from django.db import models
from django.contrib.auth import get_user_model
from user.models import Profile, get_filename
from datetime import datetime
from django_countries import countries

USER_MODEL = get_user_model()

class TestProfileModel(TestCase):
    """
    Things to test:
    - Does it include an image field for profile picture?
    - Does it include a bio?
    - Is the profile linked to the correct user?
    - Does the __str__ give the expected result?
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = USER_MODEL.objects.create_user(
            first_name='Jane',
            last_name='Doe',
            email='janedoe@test.com',
            username='janedoe',
            password='password123'
        )

        cls.profile = Profile.objects.create(
            user=cls.user,
            bio='Jane Doe is a Ruby on Rails developer from Manchester.'
        )

    def test_user_bio(self):
        """ Tests we can create a user profile with a bio, linked to a user. """
        self.assertEqual(self.profile.bio, 'Jane Doe is a Ruby on Rails developer from Manchester.')
        self.assertEqual(self.profile.user.first_name, 'Jane')

    def test_user_link(self):
        """ Tests that we can access the profile from the user object."""
        self.assertTrue(self.user, 'profile')
        self.assertEqual(self.user.profile.bio, 'Jane Doe is a Ruby on Rails developer from Manchester.')

    def test_str(self):
        """ Tests the __str__ representation. """

        expected_str = 'Jane Doe (janedoe) | janedoe@test.com'
        self.assertEqual(str(self.profile), expected_str)

    def test_profile_picture_placeholder(self):
        """ Tests that a profile picture property exists. """

        self.assertTrue(hasattr(self.profile, "profile_picture"))

        picture_field = Profile._meta.get_field("profile_picture")

        self.assertTrue(isinstance(picture_field, models.ImageField))

    def test_get_filename(self):
        """ Tests that uploaded images get a custom filename based on author's username and the post's creation date"""

        path = get_filename(self,'arbitraryfilename.jpg')

        t = datetime.now()
        datetime_str = f"{t.year}-{t.month}-{t.day}-{t.hour}{t.minute}{t.second}"

        username = self.user.username
        expected_path = f"uploads/profiles/{self.user.username}_{datetime_str}.jpg"

        self.assertEqual(path, expected_path)

    def test_get_location(self):
        """ Tests the get_location method returns nothing if city & country are undefined """

        location = self.profile.get_location()

        self.assertEqual(location, None)

    def test_get_location_city_only(self):
        """ Tests that get_location returns city """

        self.profile.city = 'Sheffield'
        self.profile.save()
        location = self.profile.get_location()

        self.assertEqual(location, 'Sheffield')

    def get_location_country_only(self):
        """ Tests that get_location returns country name"""

        self.profile.city = None
        self.profile.country = 'GB'
        self.profile.save()

        location = self.profile.get_location()
        self.assertEqual(location, 'United Kingdom')

    def get_location_country_only(self):
        """ Tests that get_location returns country name"""

        self.profile.city = 'Sheffield'
        self.profile.country = 'GB'
        self.profile.save()

        location = self.profile.get_location()
        self.assertEqual(location, 'Sheffield, United Kingdom')

