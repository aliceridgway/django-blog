from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponse
from user.models import Profile
from user.forms import PhotoForm
import json

USER_MODEL = get_user_model()

@login_required
def change_profile_picture(request, username):

    user = USER_MODEL.objects.get(username=username)
    user_profile_exists = hasattr(user, 'profile')

    if user != request.user:
        raise Http404('This page does not exist')

    if request.method != 'POST':
        raise Http404('This page does not exist')

    else:
        if user_profile_exists:
            profile = get_object_or_404(Profile, user=user)
            form = PhotoForm(request.POST, request.FILES, instance=profile)
        else:
            form = PhotoForm(request.POST, request.FILES)

        if form.is_valid():

            profile = form.save(user, commit=False)
            response = {
                'status': 'SUCCESS',
                'photo_url': profile.profile_picture.url
            }
            return HttpResponse(json.dumps(response), content_type='application/json')
        else:
            return HttpResponse('Form Invalid')

