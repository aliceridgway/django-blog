from blog.models import Post, Like, Comment, get_filename
from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.
USER_MODEL = get_user_model()


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
        cls.user = USER_MODEL.objects.create_user(
            email='janedoe@test.com',
            first_name='Jane',
            last_name='Doe',
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

        self.assertEqual(str(self.post), 'My blog post | by user123')

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
        cls.user = USER_MODEL.objects.create_user(
            email='janedoe@test.com',
            first_name='Jane',
            last_name='Doe',
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

        path = get_filename(self.post, 'arbitraryfilename.jpg')

        t = self.post.created
        datetime_str = f"{t.year}-{t.month}-{t.day}-{t.hour}{t.minute}{t.second}"

        username = self.post.author.username
        expected_path = f"uploads/{username}_{datetime_str}.jpg"

        self.assertEqual(path, expected_path)


class TestLikeModel(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.u1 = USER_MODEL.objects.create_user(
            first_name='Michael',
            last_name='R',
            username='michaelr',
            email='michael@test.com',
            password='password123'
        )

        cls.u2 = USER_MODEL.objects.create_user(
            first_name='Kate',
            last_name='S',
            username='katewrites',
            email='kate@test.com',
            password='password123'
        )
        cls.post = Post.objects.create(
            author=cls.u2,
            title='My Test Post',
            body='This is my test post'
        )
        cls.like = Like.objects.create(
            user_from=cls.u1.profile,
            user_to=cls.u2.profile,
            post=cls.post
        )

    def test_like_instance(self):
        """ Tests we can instantiate follow object """

        self.assertTrue(hasattr(self.like, 'user_from'))
        self.assertTrue(hasattr(self.like, 'user_to'))
        self.assertTrue(hasattr(self.like, 'timestamp'))
        self.assertEqual(self.like.user_from, self.u1.profile)

    def test_like_str(self):
        """ Tests string representation of follow object """

        expected_str = 'michaelr liked a post by katewrites'
        self.assertEqual(str(self.like), expected_str)

    def test_notification_str(self):
        """ Tests how event will be represented in a notification """

        expected_str = 'michaelr liked My Test Post.'

        self.assertEqual(self.like.get_notification_str(), expected_str)


class TestCommentModel(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.u1 = USER_MODEL.objects.create_user(
            first_name='Michael',
            last_name='R',
            username='michaelr',
            email='michael@test.com',
            password='password123'
        )

        cls.u2 = USER_MODEL.objects.create_user(
            first_name='Kate',
            last_name='S',
            username='katewrites',
            email='kate@test.com',
            password='password123'
        )
        cls.post = Post.objects.create(
            author=cls.u2,
            title='My Test Post',
            body='This is my test post'
        )
        cls.comment = Comment.objects.create(
            user_from=cls.u1.profile,
            user_to=cls.u2.profile,
            post=cls.post,
            body='I enjoyed reading this post.'
        )

    def test_comment_instance(self):
        """ Tests we can instantiate follow object """

        self.assertTrue(hasattr(self.comment, 'user_from'))
        self.assertTrue(hasattr(self.comment, 'user_to'))
        self.assertTrue(hasattr(self.comment, 'timestamp'))
        self.assertEqual(self.comment.user_from, self.u1.profile)

    def test_comment_str(self):
        """ Tests string representation of follow object """

        expected_str = 'michaelr commented on a post by katewrites'
        self.assertEqual(str(self.comment), expected_str)

    def test_notification_str(self):
        """ Tests how event will be represented in a notification """

        expected_str = 'michaelr commented on My Test Post.'

        self.assertEqual(self.comment.get_notification_str(), expected_str)
