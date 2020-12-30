from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import Http404, HttpResponse, JsonResponse
from user.models import Profile, Follower
from user.forms import PhotoForm, CoverPhotoForm
import json

USER_MODEL = get_user_model()


@require_POST
@login_required
def change_profile_picture(request, username):

    user = USER_MODEL.objects.get(username=username)

    if user != request.user:
        raise Http404('This page does not exist')

    if request.method != 'POST':
        raise Http404('This page does not exist')

    else:
        profile = get_object_or_404(Profile, user=user)
        form = PhotoForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():

            profile = form.save(user, commit=False)
            response = {
                'status': 'SUCCESS',
                'photo_url': profile.profile_picture.url
            }
            return HttpResponse(json.dumps(response), content_type='application/json')

        else:
            raise ValidationError('Form Invalid')


@require_POST
@login_required
def change_cover_photo(request):

    profile = get_object_or_404(Profile, user=request.user)
    form = CoverPhotoForm(request.POST, request.FILES, instance=profile)

    if form.is_valid():
        profile = form.save(request.user, commit=False)
        response = {
            'status': 'SUCCESS',
            'photo_url': profile.cover_photo.url
        }
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        raise ValidationError('Form Invalid')


@require_POST
@login_required
def toggle_user_follow(request):

    user_id = request.POST.get('id')
    action = request.POST.get('action')

    if user_id and action:
        try:
            user = USER_MODEL.objects.get(id=user_id)
            if action == 'follow':
                Follower.objects.get_or_create(
                    user_from=request.user.profile,
                    user_to=user.profile
                )
            else:
                Follower.objects.filter(user_from=request.user.profile, user_to=user.profile).delete()
        except USER_MODEL.DoesNotExist:
            return JsonResponse({'status': 'error'})

    return JsonResponse({'status': 'error'})
