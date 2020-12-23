
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from .models import User
# Create your views here.

USER_MODEL = get_user_model()

class Register(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('index')

