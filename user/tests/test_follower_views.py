from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

USER_MODEL = get_user_model()


class TestFollowViews(TestCase):
    """
    Things to test:
    - Is a request to follow successful?
    - Are non-logged-in users blocked?
    """

    @classmethod
    def setUpTestData(cls):
        cls.famous_writer = USER_MODEL.objects.create(
            first_name='Famous',
            last_name='Writer',
            username='famouswriter',
            email='famouswriter@test.com',
            password='iamabigshot'
        )

        cls.fan = USER_MODEL.objects.create(
            first_name='Jane',
            last_name='Doe',
            username='janecodes',
            email='janedoe@test.com',
            password='password123'
        )

        cls.client = Client()
        cls.follow_url = reverse('follow')

    def test_post_request(self):
        """ Tests that a request for Jane Doe to follow the famous writer is successful."""

        self.client.force_login(self.fan)

        form_data = {
            'action': 'follow',
            'id': self.fan.id
        }
        response = self.client.post(self.follow_url, form_data)

        self.assertEqual(response.status_code, 200)

    def test_login_requirement(self):
        """ Tests that a non-logged in user is redirected."""

        form_data = {
            'action': 'follow',
            'id': self.fan.id
        }
        response = self.client.post(self.follow_url, form_data)

        self.assertEqual(response.status_code, 302)

    def test_non_post_request(self):
        """ Tests that requests other than POST are rejected """

        response = self.client.get(self.follow_url)

        self.assertGreaterEqual(response.status_code, 400)
        self.assertLessEqual(response.status_code, 500)
