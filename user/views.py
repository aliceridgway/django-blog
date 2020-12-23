from .forms import CustomUserCreationForm, ProfileForm
from django.urls import reverse_lazy
from django.http import Http404
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

USER_MODEL = get_user_model()

# def profile(request, username):

#     user = USER_MODEL.objects.get(username=username)

#     if user != request.user:
#         raise Http404('This page does not exist')

#     if request.method == 'POST':
#         # form = ProfileForm(request.POST, request=request)
#         # if form.is_valid():
#         #     profile = Profile(
#         #         bio=request.POST['bio']
#         #         user=request.user
#         #     )
#     else:
#         user_profile_exists = hasattr(user, 'profile')

#         if user_profile_exists:
#             # If the user already has a profile set up, populate the form fields so a user can edit them.
#             profile = Profile.objects.get(user=user)
#             form = ProfileForm(instance=profile)
#         else:
#             # If there is no existing user profile, give the user a blank form.
#             form = ProfileForm()

#     context = {
#         'page-title':user.username,
#         'form': form,
#     }

@login_required
def profile(request, username):

    user = USER_MODEL.objects.get(username=username)

    if user != request.user:
        raise Http404('This page does not exist')

    context = {
        'page-title': user.username,
    }

    return render(request, 'user/profile.html', context)


class Register(CreateView):
    model = USER_MODEL
    form_class = CustomUserCreationForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('index')
