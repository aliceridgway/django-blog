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

    def test_profile_edit_form(self):
        """ Tests that a user with an existing profile can edit."""

        self.client.force_login(self.user)
        response = self.client.get(self.url)

        form = response.context.get('form', {})

        self.assertIn('form', response.context)
        self.assertEqual(form.instance.bio, 'Jane Doe is a Django developer from Manchester.')

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

        response = self.client.get(reverse('profile', args=[new_user.username]))
        form = response.context['form']

        self.assertFalse(hasattr(new_user, 'profile'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertEqual(form.instance.user, None)

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
        self.assertEqual(profile.bio, "Hi, I'm Charlotte. I like books and code.")


