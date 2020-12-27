from .forms import CustomUserCreationForm, ProfileForm
from .models import Profile
from django.urls import reverse_lazy, reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

USER_MODEL = get_user_model()

@login_required
def profile(request, username):
    """
    A view to create/edit a user profile.

    POST: checks if the form is valid and saves profile object.

    GET: if a profile already exists, populate a form instance with the current profile. Otherwise, give the user a blank form.
    """

    user = USER_MODEL.objects.get(username=username)
    user_profile_exists = hasattr(user, 'profile')

    if user != request.user:
        raise Http404('This page does not exist')

    if request.method == 'POST':

        if user_profile_exists:
            profile = get_object_or_404(Profile, user=user)
            form = ProfileForm(request.POST, instance=profile)
        else:
            form = ProfileForm(request.POST)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()

            success_url = reverse('author', args=[user.username])
            return HttpResponseRedirect(success_url)

    if request.method == 'GET':

        if user_profile_exists:
            profile = Profile.objects.get(user=user)
            form = ProfileForm(instance=profile)
        else:
            form = ProfileForm()

    context = {
        'page-title': user.username,
        'form': form,
        'photo_upload_url': reverse('change_profile_picture', args=[user.username])
    }

    return render(request, 'user/profile.html', context)


class Register(CreateView):
    model = USER_MODEL
    form_class = CustomUserCreationForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('index')
