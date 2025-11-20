from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import User


class UserLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('restaurant:dashboard')


class RegisterView(CreateView):
    model = User
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')


def logout_view(request):
    logout(request)
    return redirect('accounts:login')
