from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
import datetime

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

@login_required
def publish_post(request, username, slug):
    """ Changes the status to published and assigns a published date """

    post = get_object_or_404(Post, author__username=username, slug=slug)
    post.status = 'published'
    post.published = datetime.datetime.now()
    post.save()

    redirect_url = reverse('post_detail', args=[username, slug])

    return HttpResponseRedirect(redirect_url)

def post_detail(request, username, slug):
    """ Displays a post """

    return HttpResponse('Hi from post detail')


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
        return reverse('draft', args=[author.username, slug])

class EditPost(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/edit.html'
    fields = ['title', 'body']

    def get_success_url(self):
        author = self.object.author
        slug = self.object.slug
        return reverse('draft', args=[author.username, slug])