from django.test import TestCase
from userprofile.forms import ProfileForm


PROFILE_FIELDS = ['bio', 'blog_title', 'city', 'country', 'website', 'twitter', 'github']


class TestProfileForm(TestCase):

    def test_fields(self):
        """ Tests all desired fields are present on the form. """

        form = ProfileForm()

        for field in PROFILE_FIELDS:
            self.assertIn(field, form.fields)
