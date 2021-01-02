from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from blog.models import Post
from django.urls import reverse


USER_MODEL = get_user_model()


class TestComment(TestCase):
    """
    Things to test:
    - Are only POST requests accepted?
    - Are comments from non-logged in users rejected?
    - Can logged-in users leave comments?
    - Are authors blocked from leaving comments on their own post?
    """

    @classmethod
    def setUpTestData(cls):

        cls.reader = USER_MODEL.objects.create_user(
            first_name='Jane',
            last_name='Doe',
            email='janedoe@test.com',
            username='janedoe',
            password='password123'
        )
        cls.author = USER_MODEL.objects.create_user(
            first_name='Tom',
            last_name='Thomas',
            email='tomthomas@test.com',
            username='tomthomas',
            password='password123'
        )
        cls.post = Post.objects.create(
            title='Test Title',
            body='Test text',
            author=cls.author
        )
        cls.url = reverse('add_comment')
        cls.client = Client()

    def test_get_fails_4xx(self):
        """ Tests that a get request returns a 4xx status code """

        response = self.client.get(self.url)

        self.assertGreaterEqual(response.status_code, 400)
        self.assertLessEqual(response.status_code, 500)

    def test_login_requirement(self):
        """ Tests non-logged in users are blocked """
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)

    def test_author_blocked(self):
        """ Tests author cannot comment on own post """
        self.client.force_login(self.author)

        with self.assertRaises(ValueError):
            self.client.post(self.url)

    def test_post_comment(self):
        """ Tests another user can post a comment """
        self.client.force_login(self.reader)

        form_data = {
            'body': 'This post was very helpful',
            'post_id': self.post.id,
        }

        response = self.client.post(self.url, form_data)

        self.assertEqual(response.status_code, 200)
