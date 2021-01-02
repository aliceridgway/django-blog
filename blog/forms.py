from django import forms
from .models import Post, Comment
from django_summernote.widgets import SummernoteWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'feature_image',)
        widgets = {
            'body': SummernoteWidget(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)