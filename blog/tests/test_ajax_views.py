from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from blog.models import Post, Comment
from django.urls import reverse
import json

USER_MODEL = get_user_model()


class TestGetComments(TestCase):
    """
    Tests functionality to load comments on post-detail pages over AJAX.
    - Does a get request return a 200 status code?
    - Are comments excluded from the post_detail view context?
    """

    @classmethod
    def setUpTestData(cls):
        cls.author = USER_MODEL.objects.create_user(
            first_name='Tom',
            last_name='Thomas',
            email='tomthomas@test.com',
            username='tomthomas',
            password='password123'
        )
        cls.reader = USER_MODEL.objects.create_user(
            first_name='Jane',
            last_name='Doe',
            email='janedoe@test.com',
            username='janedoe',
            password='password123'
        )
        cls.post = Post.objects.create(
            title='My post',
            body='this is a post',
            author=cls.author
        )
        cls.comment1 = Comment.objects.create(
            user_from=cls.reader.profile,
            user_to=cls.author.profile,
            post=cls.post,
            body='This is a comment'
        )
        cls.comment2 = Comment.objects.create(
            user_from=cls.reader.profile,
            user_to=cls.author.profile,
            post=cls.post,
            body='comment 2'
        )
        cls.comment3 = Comment.objects.create(
            user_from=cls.reader.profile,
            user_to=cls.author.profile,
            post=cls.post,
            body='comment 3'
        )
        cls.url = reverse('get_comments', args=[cls.post.id])
        cls.post_url = reverse('post_detail', args=[cls.post.author.username, cls.post.slug])
        cls.client = Client()

    def test_get_request(self):
        """ Tests a request to fetch comments for a given post is successful """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_comments_excluded_from_post_detail(self):
        """ Tests that comments are not included in the context for the post-detail view """
        response = self.client.get(self.post_url)

        self.assertNotIn('comments', response.context)

    def test_response_structure(self):
        """ Tests JSON structure of response:
        We need to know the comment text, the name of the user who wrote it and when it was written.
        """
        response = self.client.get(self.url)
        json_response = json.loads(response.content)

        self.assertIn('comments', json_response)
        self.assertIn('status', json_response)

        comment = json_response['comments'][0]

        self.assertIn('user_from', comment)
        self.assertIn('body', comment)
        self.assertIn('timestamp', comment)

        user = comment['user_from']

        self.assertIn('first_name', user)
        self.assertIn('last_name', user)

    def test_response_comments(self):
        """ Tests the response contains an array of three comments"""

        response = self.client.get(self.url)
        json_response = json.loads(response.content)

        self.assertTrue(isinstance(json_response['comments'], list))
        self.assertEqual(len(json_response['comments']), 3)


class TestAddComment(TestCase):
    """
    Tests ability to submit comments on the post-detail page over AJAX
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
