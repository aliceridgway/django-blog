import datetime
from .models import Post
from django.test import TestCase
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
        """ Tests two posts with identical titles receive different slugs """
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
