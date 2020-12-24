from .forms import CustomUserCreationForm, ProfileForm
from .models import Profile
from django.urls import reverse_lazy, reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
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
        form = ProfileForm(request.POST)

        if form.is_valid():
            if user_profile_exists:
                # Update profile
                user.profile.bio = request.POST['bio']
                user.profile.save()
            else:
                # Create profile
                profile = Profile.objects.create(
                    user=user,
                    bio=request.POST['bio']
                )

            success_url = reverse('author', args=[username])
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
    }

    return render(request, 'user/profile.html', context)


class Register(CreateView):
    model = USER_MODEL
    form_class = CustomUserCreationForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('index')
