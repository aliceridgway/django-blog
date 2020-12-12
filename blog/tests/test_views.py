import datetime
from blog.models import Post
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


class TestIndexView(TestCase):

    """ Things to test: """
    """ 1. Does the GET request work?"""
    """ 2. Does the context contain a key for 'posts'?"""
    """ 3. Are draft posts excluded? """
    """ 4. Are posts ordered by date (most recent first)? """

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


class TestAddPostView(TestCase):

    """ Things to test: """
    """ 1. Does the url work?"""
    """ 2. If a user isn't logged in, are they redirected?"""
    """ 3. Are the correct form fields displayed? """
    """ 4. When a post is saved, does it redirect to the preview page? """

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = reverse('add')
        user = User(username='testuser', password='password123')
        user.save()

    def test_get_add(self):
        """ Test that a GET request works and renders the correct template"""

        user = User.objects.get(username='testuser')
        self.client.force_login(user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/add.html')

    def test_user_must_be_logged_in(self):
        """ Test that a non-logged in user is redirected """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_form_fields(self):
        """ Test that only title and body fields are displayed in the user form"""

        user = User.objects.get(username='testuser')
        self.client.force_login(user)
        response = self.client.get(self.url)
        form = response.context_data['form']

        self.assertEqual(len(form.fields), 2)
        self.assertIn('title', form.fields)
        self.assertIn('body', form.fields)

    def test_success_url(self):
        """ Test that submitting the form redirects to the preview page """

        user = User.objects.get(username='testuser')
        self.client.force_login(user)

        form_data = {
            'title':'my title',
            'body':'This is the post body',
        }
        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/testuser/my-title/draft')


class TestDraftView(TestCase):
    """
    Things to test:
     - Does the GET request work?
     - Does the context include a post?
     - Are non-logged-in users barred?
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='user123',
            password='password456'
        )
        cls.post = Post.objects.create(
            title='my title',
            body='post body',
            author=cls.user
        )
        cls.client = Client()
        cls.url = reverse('draft', args=[cls.user.username, cls.post.slug])

    def test_login_requirement(self):
        """ Tests that a non-logged-in user is redirected """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_get_draft(self):
        """ Tests that a GET request works"""
        user = User.objects.get(username='user123')
        self.client.force_login(user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/draft.html')

    def test_draft_context(self):
        """ Tests that there's a post included in the context"""
        user = User.objects.get(username='user123')
        self.client.force_login(user)
        response = self.client.get(self.url)
        post = response.context['post']

        self.assertEqual(post.title, 'my title')
        self.assertEqual(post.body, 'post body')


class TestEditPostView(TestCase):
    """
    Things to test:
    1. Are non-logged-in users redirected?
    2. Do logged in users receive a 200 status code?
    3. On save, are they redirected to the draft page?
    4. When the title is updated, does the slug update as well?
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='user123',
            password='password456'
        )
        cls.post = Post.objects.create(
            title='my title',
            body='post body',
            author=cls.user
        )
        cls.client = Client()
        cls.url = '/user123/my-title/edit'

    def test_user_must_be_logged_in(self):
        """ Tests that a non-logged in user is redirected """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_get_request(self):
        """ Tests that a logged in user receives a 200"""
        user = User.objects.get(username='user123')
        self.client.force_login(user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/edit.html')

    def test_success_url(self):
        """
        Tests that the user is redirected to the draft page on save.
        Tests that the url's slug is correct for an updated title.
        """

        user = User.objects.get(username='user123')
        self.client.force_login(user)

        redirect_url = reverse('draft', args=[user.username, 'new-title'])

        post = {
            'title':'new title',
            'body': 'new bit of text',
            'author': user
        }

        response = self.client.post(self.url, post)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


class TestPublishView(TestCase):
    """
    Things to test:
    - Are non-logged-in users blocked?
    For logged in users:
    - Does the view change the post's status to 'published'?
    - Is a published date assigned?
    - Is the user redirected to the post detail page?
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='user123',
            password='password456'
        )
        cls.post = Post.objects.create(
            title='my title',
            body='post body',
            author=cls.user
        )
        cls.client = Client()
        cls.url = '/user123/my-title/publish'

    def test_login_requirement(self):
        """ Tests a non-logged-in user is redirected to the login page"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        # TO DO:
        # Test redirect to login page when login page exists

    def test_published_status(self):
        """ Tests a post's status is changed to published """
        user = User.objects.get(username='user123')
        self.client.force_login(user)
        self.client.get(self.url)

        post = Post.objects.get(
            author=user,
            title='my title'
        )
        self.assertEqual(post.status, 'published')

    def test_published_status(self):
        """ Tests a post has a publication date """
        user = User.objects.get(username='user123')
        self.client.force_login(user)
        self.client.get(self.url)

        post = Post.objects.get(
            author=user,
            title='my title'
        )

        now = datetime.datetime.now()

        self.assertIsInstance(post.published, datetime.datetime )
        self.assertEqual(now.year, post.published.year)
        self.assertEqual(now.month, post.published.month)
        self.assertEqual(now.day, post.published.day)


class TestPostDetail(TestCase):
    """
    Things to test:
    - A non-logged-in user is shown a 404 for a draft post
    - A logged in user attempting to see their own draft post is redirected to drafts page
    - A GET request is successful for published posts
    - Context contains a post
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='user123',
            password='password456'
        )
        cls.user2 = User.objects.create(
            username='user2',
            password='password123'
        )
        cls.draft_post = Post.objects.create(
            title='my draft title',
            body='post body',
            author=cls.user
        )
        cls.published_post = Post.objects.create(
            title='my published title',
            body='post body',
            author=cls.user,
            status='published',
            published=datetime.datetime.now()
        )
        cls.client = Client()

    def test_draft_404(self):
        """
        Tests users cannot view draft posts and get 404 instead
        """
        post_detail_url = reverse('post_detail', args=[self.draft_post.author.username, self.draft_post.slug])
        response = self.client.get(post_detail_url)

        self.assertEqual(response.status_code, 404)

    def test_published_200(self):
        """
        Tests that a request for a published post is successful
        """
        post_detail_url = reverse('post_detail', args=[self.published_post.author.username, self.published_post.slug])

        response = self.client.get(post_detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/post_detail.html')

    def test_user_draft_redirect(self):
        """
        Tests that a logged-in user attempting to view their own unpublished post is redirected to the drafts page.
        """
        user = User.objects.get(username='user123')
        self.client.force_login(user)

        post_detail_url = reverse('post_detail', args=[self.draft_post.author.username, self.draft_post.slug])
        response = self.client.get(post_detail_url)

        redirect_url = reverse('draft', args=[self.draft_post.author.username, self.draft_post.slug])

        self.assertRedirects(response, redirect_url)

    def test_user_draft_redirect_gotcha(self):
        """
        Tests that a logged in user who isn't the post author gets a 404
        """
        user = User.objects.get(username='user2')
        self.client.force_login(user)

        post_detail_url = reverse('post_detail', args=[self.draft_post.author.username, self.draft_post.slug])
        response = self.client.get(post_detail_url)

        self.assertEqual(response.status_code, 404)

    def test_post_detail_context(self):
        """
        Tests that there is a post in the response context
        """
        post_detail_url = reverse('post_detail', args=[self.published_post.author.username, self.published_post.slug])

        response = self.client.get(post_detail_url)
        post = response.context.get('post', {})

        self.assertIn('post', response.context)
        self.assertEqual(post.title, 'my published title')
