import datetime
from .models import Post
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

class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        u = User.objects.create_user(
            username='user123',
            password='password456'
        )

        Post.objects.create(title='title1', body='body1', author=u, status='draft')

        Post.objects.create(
            title='title2',
            body='body2',
            author=u,
            status='published',
            published=datetime.datetime(2018,1,1)
        )

        Post.objects.create(
            title='title3',
            body='body3',
            author=u,
            status='published',
            published=datetime.datetime(2019,1,1)
        )

        Post.objects.create(
            title='title4',
            body='body4',
            author=u,
            status='published',
            published=datetime.datetime(2020,1,1)
        )

        cls.response = Client().get(reverse('index'))

    def test_get_index(self):
        """ Test that a get request to index works and renders the correct template"""

        self.assertEquals(self.response.status_code, 200)
        self.assertTemplateUsed('blog/index.html')

    def test_context_contains_posts(self):
        """ tests that there the context contains 'posts' """

        self.assertIn('posts', self.response.context)

    def test_excludes_draft_posts(self):
        """ Test that the list of posts on the homepage excludes drafts"""

        number_of_published_posts = len(self.response.context['posts'])

        self.assertEqual(number_of_published_posts, 3)

    def test_posts_are_ordered_by_published_date(self):
        """ Tests that posts are ordered by published date starting with the most recent """
        posts = self.response.context['posts']

        year_post1 = posts[0].published.year
        year_post2 = posts[1].published.year
        year_post3 = posts[2].published.year

        self.assertGreater(year_post1, year_post2)
        self.assertGreater(year_post1, year_post3)
        self.assertGreater(year_post2, year_post3)
