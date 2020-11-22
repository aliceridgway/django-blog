from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
# Create your views here.

def index(request):

    posts = Post.objects.filter(status='published').order_by('-published')

    context = {
        'posts': posts
    }
    return render(request, 'blog/index.html', context)