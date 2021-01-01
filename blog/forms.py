from django import forms
from .models import Post
from django_summernote.widgets import SummernoteWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'feature_image',)
        widgets = {
            'body': SummernoteWidget(),
        }
