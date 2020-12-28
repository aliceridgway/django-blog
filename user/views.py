from .forms import CustomUserCreationForm, ProfileForm
from .models import Profile
from django.urls import reverse_lazy, reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

USER_MODEL = get_user_model()


@login_required
def edit_profile(request, username):
    """ A view to edit a user profile """

    user = USER_MODEL.objects.get(username=username)

    if user != request.user:
        raise Http404('This page does not exist')

    if request.method == 'POST':
        profile = get_object_or_404(Profile, user=user)
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()

            success_url = reverse('author', args=[user.username])

            return HttpResponseRedirect(success_url)

    else:
        profile = Profile.objects.get(user=user)
        form = ProfileForm(instance=profile)

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
