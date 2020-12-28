from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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

    def test_profile_create(self):
        """ Tests that a new user can create a profile in the same view. """

        new_user = USER_MODEL.objects.create_user(
            first_name='Charlotte',
            last_name='Bronte',
            email='charlottebronte@test.com',
            username='cbronte',
            password='pass123456'
        )

        self.client.force_login(new_user)

        response = self.client.get(
            reverse('profile', args=[new_user.username]))

        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_user_update(self):
        """ Tests that a user can update their profile """

        form_data = {
            "user": self.user,
            "bio": "This is Jane Doe's updated profile."
        }

        self.client.force_login(self.user)
        response = self.client.post(self.url, form_data)

        profile = Profile.objects.get(user=self.user)

        author_url = reverse('author', args=[self.user.username])

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, author_url)
        self.assertEqual(profile.bio, "This is Jane Doe's updated profile.")

    def test_user_create_profile(self):
        """ Tests a user can create a profile """

        new_user = USER_MODEL.objects.create_user(
            first_name='Charlotte',
            last_name='Bronte',
            email='charlottebronte@test.com',
            username='cbronte',
            password='pass123456'
        )
        self.client.force_login(new_user)

        form_data = {
            "user": new_user,
            "bio": "Hi, I'm Charlotte. I like books and code."
        }

        profile_url = reverse('profile', args=[new_user.username])
        author_url = reverse('author', args=[new_user.username])

        response = self.client.post(profile_url, form_data)
        profile = Profile.objects.get(user=new_user)

        self.assertRedirects(response, author_url)
        self.assertEqual(
            profile.bio, "Hi, I'm Charlotte. I like books and code.")


class TestProfilePhotoView(TestCase):
    """
    Things to test:
    - Does a GET request give a 404?
    - Does a POST request work?
    - Are users only able to change their own profile picture?
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

        cls.client = Client()
        cls.url = reverse('change_profile_picture', args=[cls.user.username])

    def test_get_request(self):
        """ Test that a GET request returns a 404. (This view only accepts POST requests)"""
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_login_requirement(self):
        """ Tests that a non-logged-in user has request blocked"""

        form_data = {
            'user': self.user,
            'profile_picture': open('user/tests/thePOST-default.jpg', 'rb'),
        }
        response = self.client.post(self.url, form_data)

        self.assertEqual(response.status_code, 302)

    def test_authorisation(self):
        """ Tests that users can only change their own profile picture. """

        self.client.force_login(self.hacker)

        form_data = {
            'user': self.user,
            'profile_picture': open('user/tests/thePOST-default.jpg', 'rb'),
        }
        response = self.client.post(self.url, form_data)

        self.assertEqual(response.status_code, 404)

    def test_invalid_form(self):
        """ Tests that a validation error is raised if the form is invalid."""

        self.client.force_login(self.user)

        form_data = {
            'user': self.user,
            'profile_picture': open('user/tests/thePOST-default.jpg', 'rb'),
        }

        with self.assertRaises(ValidationError):
            self.client.post(self.url, form_data)

    def test_post_request(self):
        """ Tests that POST request is successful for a logged-in user
         attempting to upload profile picture to their own profile."""

        self.client.force_login(self.user)

        form_data = {
            'profile_picture': open('user/tests/thePOST-default.jpg', 'rb'),
            'x': 0.0,
            'y': 0.0,
            'width': 20.0,
            'height': 20.0,
        }

        response = self.client.post(self.url, form_data)

        self.assertEqual(response.status_code, 200)
