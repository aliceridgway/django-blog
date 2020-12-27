from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User, Profile
from django_countries.widgets import CountrySelectWidget
from django.core.files import File
from PIL import Image


class CustomUserCreationForm(UserCreationForm):
    """
    We need to extend the default UserCreationForm to accommodate the extra fields.
    This form is displayed when we create a user in admin from another model.
    We can also reuse the form in the UI for registration.
    """
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "username")


class UserChangeForm(forms.ModelForm):
    """
    This is the form that's displayed when you edit the user. This won't affect how user information is displayed
    in admin. Instead, it controls the pop-up form when user objects are editted from another model.
    This form needs to be updated to show fields that aren't present in the AbstractBaseUser.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'password', 'last_name',
                  'username', 'is_active', 'is_admin')


class PhotoForm(forms.ModelForm):
    """
    A form for uploading profile pictures. This is used with Cropper.js on the front-end.
    x, y, width & height are supplied by Cropper.js and are used here to crop the photo
    using Pillow.
    """

    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Profile
        fields = ('profile_picture', 'x', 'y', 'width',
                  'height')

    def save(self, user, commit=True):

        profile = super().save()

        profile.user = user

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(profile.profile_picture)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(profile.profile_picture.path)

        profile.save()

        return profile


class ProfileForm(forms.ModelForm):
    """
    A form to create/update a user profile. Includes all fields apart from
    profile_picture, which is handled in PhotoForm.
    """
    class Meta:
        model = Profile
        fields = ('bio', 'city', 'country', 'website', 'twitter_username',
                  'github_username')
