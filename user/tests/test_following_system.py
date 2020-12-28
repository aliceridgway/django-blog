from django.test import TestCase
from django.contrib.auth import get_user_model
from user.models import Follower, Profile

USER_MODEL = get_user_model()


class TestFollow(TestCase):
    """
    Class to test the Follow intermediary model.
    """

    @classmethod
    def setUpTestData(cls):

        cls.famous_writer = USER_MODEL.objects.create(
            first_name='Famous',
            last_name='Writer',
            username='famouswriter',
            email='famouswriter@test.com',
            password='iamabigshot'
        )
        Profile.objects.create(
            user=cls.famous_writer
        )

        cls.fan = USER_MODEL.objects.create(
            first_name='Jane',
            last_name='Doe',
            username='janecodes',
            email='janedoe@test.com',
            password='password123'
        )
        Profile.objects.create(
            user=cls.fan
        )

        cls.follow = Follower.objects.create(
            user_from=cls.fan.profile, user_to=cls.famous_writer.profile)

    def test_follower_intermediary(self):
        """ Tests we can create a relationship between two users using the intermediary Follower model """

        self.assertTrue(hasattr(self.follow, 'created'))
        self.assertEqual(self.follow.user_to.user.username, 'famouswriter')

    def test_follower_str(self):
        """ Tests the __str__ method of the Follower model """

        self.assertEqual(str(self.follow), 'janecodes follows famouswriter')


class TestProfileFollowing(TestCase):
    """ Tests the following property of the Profile model """

    @classmethod
    def setUpTestData(cls):

        cls.famous_writer = USER_MODEL.objects.create(
            first_name='Famous',
            last_name='Writer',
            username='famouswriter',
            email='famouswriter@test.com',
            password='iamabigshot'
        )

        cls.fan = USER_MODEL.objects.create(
            first_name='Jane',
            last_name='Doe',
            username='janecodes',
            email='janedoe@test.com',
            password='password123'
        )

        cls.famous_writer_profile = Profile.objects.create(
            user=cls.famous_writer
        )

        cls.fan_profile = Profile.objects.create(
            user=cls.fan
        )

        cls.event = Follower.objects.create(
            user_from=cls.fan.profile,
            user_to=cls.famous_writer.profile
        )

    def test_writer_followers(self):
        """ Tests that the famous writer now has Jane Doe as a follower """

        followers = self.famous_writer.profile.followers.all()

        self.assertEqual(followers.count(), 1)
        self.assertEqual(followers.first().user.username, 'janecodes')

    def test_fan_following(self):
        """ Tests the famous writer has been added to Jane Doe's followers. """

        following = self.fan.profile.following.all()

        self.assertEqual(following.count(), 1)
        self.assertEqual(following.first().user.username, 'famouswriter')

    def test_following_is_not_mutual(self):
        """ Tests that the famous writer isn't inadvertantly following Jane Doe """

        fan_followers = self.fan.profile.followers
        famous_writer_following = self.famous_writer.profile.following

        self.assertEqual(fan_followers.count(), 0)
        self.assertEqual(famous_writer_following.count(), 0)
