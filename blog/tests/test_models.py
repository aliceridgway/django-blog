import datetime
from blog.models import Post, get_filename
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

# Create your tests here.

class TestPostModel(TestCase):
    """
    Things to test:
    - Can be create a post with the bare minimum of fields? (Title, body and author)
    - Does the __str__ method behave as expected?
    - Is a slug automatically created?
    - Do two posts with the same title and user get different slugs?
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='user123',
            password='password456'
        )

        cls.post = Post.objects.create(
            title='My blog post',
            body='This is my first post',
            author=cls.user,
        )

    def test_create_post(self):
        """ Tests that a post with a title, body, user and creation date can be created"""

        self.assertEqual(self.post.title, 'My blog post')
        self.assertEqual(self.post.author, self.user)


    def test_post_str(self):
        """ Tests the __str__ of the Post model"""

        self.assertEqual(str(self.post),'My blog post | by user123')

    def test_creates_a_slug(self):
        """ Tests a slug is automatically created """

        self.assertEqual(self.post.slug, 'my-blog-post')

    def test_slugs_are_unique(self):
        """ Tests two posts with identical titles from the same author receive different slugs """

        second_title = Post.objects.create(
            title='My blog post',
            body='This is my second post',
            author=self.user,
        )

        self.assertNotEqual(self.post.slug, second_title.slug)

class TestFeatureImages(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='user1',
            password='password123'
        )

        cls.post = Post.objects.create(
            title='my title',
            body='post body',
            author=cls.user
        )

    def test_get_filename(self):
        """ Tests that uploaded images get a custom filename based on author's username and the post's creation date"""

        path = get_filename(self.post,'arbitraryfilename.jpg')

        t = self.post.created
        datetime_str = f"{t.year}-{t.month}-{t.day}-{t.hour}{t.minute}{t.second}"

        username = self.post.author.username
        expected_path = f"uploads/{username}_{datetime_str}.jpg"

        self.assertEqual(path, expected_path)
