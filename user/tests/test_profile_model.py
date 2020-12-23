from django.test import TestCase
from django.contrib.auth import get_user_model
from user.models import Profile

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
        expected_str = 'Jane Doe (janedoe) | janedoe@test.com'
        self.assertEqual(str(self.profile), expected_str)