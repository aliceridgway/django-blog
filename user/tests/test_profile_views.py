from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from user.models import Profile

USER_MODEL = get_user_model()

class TestProfileView(TestCase):
    """
    Things to test:
    - Does the logged-in profile owner get a 200 response?
    - Does a non-logged-in user get redirected to the login screen?
    - Are logged-in users blocked from seeing profiles that aren't their own?

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
        cls.hacker = USER_MODEL.objects.create_user(
            first_name='Hacker',
            last_name='McHackerson',
            email='hacker@test.com',
            username='hacker',
            password='password456'
        )
        cls.user_profile = Profile.objects.create(
            user=cls.user,
            bio = 'Jane Doe is a Django developer from Manchester.'
        )
        cls.client = Client()
        cls.url = reverse('profile', args=[cls.user.username])

    def test_login_requirement(self):
        """ Tests that non-logged in users are redirected to the login page."""

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_user_can_see_own_profile(self):
        """ Tests a user can view their own profile. """

        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'user/profile.html')
        self.assertEqual(response.status_code, 200)

    def test_profile_privacy(self):
        """ Tests users cannot see profiles of other users. """

        self.client.force_login(self.hacker)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)