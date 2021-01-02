from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from blog.models import Post, Comment
from django.urls import reverse


USER_MODEL = get_user_model()


class TestAddComment(TestCase):
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


class TestDeleteComment(TestCase):
    """
    Things to test:
    - Are only POST requests accepted?
    - Are comments from non-logged in users rejected?
    - Can logged-in users leave comments?
    - Is the deletion attempt definitely by the comment author?
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
        cls.comment = Comment.objects.create(
            user_from=cls.reader.profile,
            user_to=cls.author.profile,
            post=cls.post,
            body='Great post!'
        )
        cls.url = reverse('delete_comment')
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

    def test_authorisation(self):
        """ Tests that comments can only be deleted by the user who wrote it"""

        hacker = USER_MODEL.objects.create_user(
            first_name='Tom',
            last_name='Thomas',
            email='hacker@test.com',
            username='hacker',
            password='password123'
        )
        self.client.force_login(hacker)

        form_data = {
            'comment_id': self.comment.id
        }

        response = self.client.post(self.url, form_data)

        self.assertGreaterEqual(response.status_code, 400)
        self.assertLessEqual(response.status_code, 500)

    def test_delete_comment(self):
        """ Tests readers can delete their comments """

        self.client.force_login(self.reader)

        form_data = {
            'comment_id': self.comment.id
        }

        response = self.client.post(self.url, form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Comment.objects.all().exists())
