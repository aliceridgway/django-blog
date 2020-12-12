from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
# Create your views here.

def index(request):

    posts = Post.objects.filter(status='published').order_by('-published')

    context = {
        'posts': posts
    }
    return render(request, 'blog/index.html', context)

def draft(request, username, slug):

    post = Post.objects.get(author__username=username, slug=slug)
    context = {
        'post': post,
    }

    return render(request, 'blog/draft.html', context)

class AddPost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/add.html'
    fields = ['title', 'body']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        author = self.object.author
        slug = self.object.slug
        return reverse('draft', args=[author, slug])
