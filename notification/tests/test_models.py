from django.test import TestCase
from django.contrib.auth import get_user_model
from notification.models import Follow, Comment, Like
from blog.models import Post

USER_MODEL = get_user_model()


class TestFollowModel(TestCase):

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
        cls.follow = Follow.objects.create(
            user_from=cls.u1.profile,
            user_to=cls.u2.profile
        )

    def test_follow_instance(self):
        """ Tests we can instantiate follow object """

        self.assertTrue(hasattr(self.follow, 'user_from'))
        self.assertTrue(hasattr(self.follow, 'user_to'))
        self.assertTrue(hasattr(self.follow, 'timestamp'))
        self.assertEqual(self.follow.user_from, self.u1.profile)

    def test_follow_str(self):
        """ Tests string representation of follow object """

        expected_str = 'michaelr followed katewrites'
        self.assertEqual(str(self.follow), expected_str)

    def test_notification_str(self):
        """ Tests how event will be represented in a notification """

        expected_str = 'michaelr followed you.'

        self.assertEqual(self.follow.get_notification_str(), expected_str)


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


class TestNotifications(TestCase):
    """
    Things to test:
    - Can we access notifications from the user's profile?
    - Do Like, Follow and Comment events create Notification instances?
    - Do the notifications belong to the correct user?
    - Do the notifications have a timestamp?
    """

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
            title='Test Title',
            body='test body',
            author=cls.u2
        )

    def test_notifications_exist(self):
        """ Tests the profile has an attribute called notifications """
        self.assertTrue(hasattr(self.u2.profile, 'notifications'))

    def test_notifications_empty(self):
        """ Tests that notifications is initially an empty queryset """
        self.assertEqual(self.u2.profile.notifications.count(), 0)

    def test_like_notification(self):
        """ Tests a notification is created when a new like event is saved. """

        Like.objects.create(
            user_from=self.u1.profile,
            user_to=self.u2.profile,
            post=self.post
        )

        notification = self.u2.profile.notifications.first()

        self.assertEqual(notification.profile, self.u2.profile)
        self.assertEqual(notification.message, 'michaelr liked Test Title.')
        self.assertTrue(hasattr(notification, 'timestamp'))

        notification.delete()

    def test_follow_notification(self):
        """ Tests that a notification is created when a new follow event is saved"""

        Follow.objects.create(
            user_from=self.u1.profile,
            user_to=self.u2.profile
        )

        notification = self.u2.profile.notifications.first()

        self.assertEqual(notification.profile, self.u2.profile)
        self.assertEqual(notification.message, 'michaelr followed you.')
        self.assertTrue(hasattr(notification, 'timestamp'))

        notification.delete()

    def test_comment_notification(self):
        """ Tests that a notification is created when a new comment is saved. """

        Comment.objects.create(
            user_from=self.u1.profile,
            user_to=self.u2.profile,
            post=self.post,
            body='I like this post'
        )

        notification = self.u2.profile.notifications.first()

        self.assertEqual(notification.profile, self.u2.profile)
        self.assertEqual(notification.message, 'michaelr commented on Test Title.')
        self.assertTrue(hasattr(notification, 'timestamp'))

        notification.delete()
