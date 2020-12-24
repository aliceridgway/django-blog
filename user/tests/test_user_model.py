from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import models
from datetime import datetime, timezone
from django.db import IntegrityError
from django.core.exceptions import ValidationError

class TestUserManager(TestCase):
    """ Things to test:
    - Can we create a user with create_user?
    - Can we create a superuser with create_superuser?
    - Are special characters in the username blocked? (the username will go in urls so a '/' could cause issues)
    - Are users blocked from creating two accounts with the same email?
    - Is the uniqueness of usernames enforced?
    - Is a date/time saved when a user is created?
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            email='janedoe@test.com',
            password='pass123',
            username='Jane-d_codes',
            first_name='Jane',
            last_name='Doe',
        )

        cls.superuser = get_user_model().objects.create_superuser(
            email='superuser@test.com',
            password='pass456',
            username='thesuperuser',
            first_name='Super',
            last_name='User'
        )

    def test_create_user(self):
        """ Tests the create_user method """

        self.assertEqual(self.user.email, 'janedoe@test.com')
        self.assertEqual(self.user.username, 'jane-d_codes')
        self.assertEqual(self.user.first_name, 'Jane')
        self.assertEqual(self.user.last_name, 'Doe')

    def test_create_superuser(self):
        """ Tests the createsuperuser method"""

        self.assertEqual(self.superuser.email, 'superuser@test.com')
        self.assertEqual(self.superuser.username, 'thesuperuser')
        self.assertEqual(self.superuser.first_name, 'Super')
        self.assertEqual(self.superuser.last_name, 'User')

    def test_username_uniqueness(self):
        """ Tests that two users cannot have the same username """

        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(
                email='janeshaw@test.com',
                password='pass123',
                username='Jane-d_coDes',
                first_name='Jane',
                last_name='Shaw',
            )

    def test_no_special_characters_in_username(self):
        """ Tests that our username is url friendly (A-Z 0-9 -_ only)"""

        # This test has room for improvement. We're only testing a sample of characters.
        bad_characters = ['/','(','?','@','#','~']

        for bad_character in bad_characters:
            with self.assertRaises(ValidationError):
                get_user_model().objects.create_user(
                    email='janeshaw@test.com',
                    password='pass123',
                    username=f'jane_co{bad_character}des',
                    first_name='Jane',
                    last_name='Shaw',
                )

    def test_username_field(self):
        """ Tests that the email is assigned as the USERNAME_FIELD """
        # Django will automatically enforce uniqueness for the USERNAME_FIELD
        self.assertEqual(get_user_model().USERNAME_FIELD, 'email')

    def test_account_created(self):
        """ Tests that a datetime is assigned to users when their account has been created. """

        self.assertTrue(hasattr(self.user, 'account_created'))
        self.assertTrue(hasattr(self.superuser, 'account_created'))

    def test_account_created_autoadd(self):
        """ Test the account_created date is roughly now """

        now = datetime.now(timezone.utc)
        user_created_at = self.user.account_created
        superuser_created_at = self.superuser.account_created

        user_diff = now - user_created_at
        superuser_diff = now - superuser_created_at

        # Testing that there's less than 10 seconds between when the user was created and when we created 'now' in this test.
        # 10 seconds is more than enough

        self.assertLessEqual(user_diff.seconds, 10)
        self.assertLessEqual(superuser_diff.seconds, 10)