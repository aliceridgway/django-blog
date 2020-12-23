from django.test import TestCase, Client
from django.shortcuts import reverse

class TestUserRegistration(TestCase):
    """
    Things to test:
    - Is the GET request successful?
    - Is the POST request successful?
    """

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('register')
        cls.client = Client()

    def test_get_request(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('user/register.html')

    def test_post_request(self):
        form_data = {
            'email': 'janedoe@test.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': 'janedoe',
            'password':'secretpassword',
            'password2':'secretpassword',
        }

        response = self.client.post(self.url, form_data)

        self.assertEqual(response.status_code, 200)
