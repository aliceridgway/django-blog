from django.test import TestCase
from django.db import models
from django.contrib.auth import get_user_model
from user.models import Profile, get_filename
from datetime import datetime

USER_MODEL = get_user_model()


class TestProfileModel(TestCase):
    """
    Things to test:
    - Is a profile instance created when a new user is created?
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

    def test_profile_creation(self):
        """ Tests that creating a user creates a profile object"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(self.user.profile.user.username, 'janedoe')

    def test_str(self):
        """ Tests the __str__ representation. """

        expected_str = 'Jane Doe (janedoe) | janedoe@test.com'

        self.assertEqual(str(self.user.profile), expected_str)

    def test_profile_picture_placeholder(self):
        """ Tests that a profile picture property exists. """

        self.assertTrue(hasattr(self.user.profile, "profile_picture"))

        picture_field = Profile._meta.get_field("profile_picture")

        self.assertTrue(isinstance(picture_field, models.ImageField))

    def test_get_filename(self):
        """ Tests that uploaded images get a custom filename based on author's username and the post's creation date"""

        path = get_filename(self, 'arbitraryfilename.jpg')

        t = datetime.now()
        datetime_str = f"{t.year}-{t.month}-{t.day}-{t.hour}{t.minute}{t.second}"

        expected_path = f"uploads/profiles/{self.user.username}_{datetime_str}.jpg"

        self.assertEqual(path, expected_path)

    def test_get_location(self):
        """ Tests the get_location method returns nothing if city & country are undefined """

        location = self.user.profile.get_location()

        self.assertEqual(location, None)

    def test_get_location_city_only(self):
        """ Tests that get_location returns city """

        self.user.profile.city = 'Sheffield'
        self.user.profile.save()
        location = self.user.profile.get_location()

        self.assertEqual(location, 'Sheffield')

    def get_location_country_only(self):
        """ Tests that get_location returns country name"""

        self.user.profile.city = None
        self.user.profile.country = 'GB'
        self.user.profile.save()

        location = self.user.profile.get_location()
        self.assertEqual(location, 'United Kingdom')

    def get_location_city_and_country(self):
        """ Tests that get_location returns country name"""

        self.user.profile.city = 'Sheffield'
        self.user.profile.country = 'GB'
        self.user.profile.save()

        location = self.user.profile.get_location()
        self.assertEqual(location, 'Sheffield, United Kingdom')
