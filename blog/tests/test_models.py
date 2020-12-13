import datetime
from blog.models import Post, get_filename
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

# Create your tests here.

class TestPostModel(TestCase):

    def setUp(self):
        User.objects.create_user(
            username='user123',
            password='password456'
        )

    def test_create_post(self):
        """ Test that a post with a title, body, user and creation date can be created"""

        user = User.objects.get(username='user123')
        post = Post(
            title='My blog post',
            body='Once upon a time...',
            slug='my-blog-post',
            author=user,
        )

        self.assertEqual(post.title, 'My blog post')
        self.assertEqual(post.author, user)


    def test_post_str(self):
        """ Tests the __str__ of the Post model"""
        user = User.objects.get(username='user123')
        post = Post(
            title='My blog post',
            body='Once upon a time...',
            slug='my-blog-post',
            created=timezone.now,
            author=user,
        )

        self.assertEqual(str(post),'My blog post | by user123')


class TestPostSlugs(TestCase):

    def setUp(self):
        User.objects.create_user(
            username='user123',
            password='password456'
        )

    def test_creates_a_slug(self):
        user = User.objects.get(username='user123')

        post = Post(
            title='My title',
            body='my post goes here',
            author=user
        )
        post.save()

        self.assertEqual(post.slug, 'my-title')

    def test_slugs_are_unique(self):
        """ Tests two posts with identical titles from the same author receive different slugs """
        user = User.objects.get(username='user123')

        post1 = Post(
            title='My title',
            body='my post goes here',
            author=user
        )
        post1.save()

        post2 = Post(
            title='My title',
            body='my post goes here',
            author=user
        )
        post2.save()

        self.assertNotEqual(post1.slug, post2.slug)

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
