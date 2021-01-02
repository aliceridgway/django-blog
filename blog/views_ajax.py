from .models import Post, Comment
from .forms import CommentForm
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import ValidationError, PermissionDenied

USER_MODEL = get_user_model()


@require_POST
@login_required
def add_comment(request):

    post_id = request.POST.get('post_id')

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise ValueError('No post found')

    if request.user != post.author:

        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user_from = request.user.profile
            comment.user_to = post.author.profile
            comment.post = post
            comment.save()

            return JsonResponse({'status': 'success'})
        else:
            raise ValidationError('Form Invalid')

    else:
        raise PermissionDenied('You are not authorised to comment')


@require_POST
@login_required
def delete_comment(request):

    comment_id = request.POST.get('comment_id')

    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        raise ValueError('This comment does not exist')

    if comment.user_from.user != request.user:
        raise PermissionDenied('Permission Denied')

    comment.delete()

    return JsonResponse({'status': 'success'})