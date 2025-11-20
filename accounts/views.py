from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import User


class UserLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        # Redirección según rol
        if hasattr(user, 'role'):
            if user.role in ['ADMIN', 'WAITER']:
                return reverse_lazy('restaurant:dashboard')
            if user.role == 'CUSTOMER':
                return reverse_lazy('restaurant:reservation_list')
        # Fallback
        return reverse_lazy('restaurant:dashboard')


class RegisterView(CreateView):
    model = User
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        user = self.object
        if hasattr(user, 'role') and user.role == 'CUSTOMER':
            return reverse_lazy('restaurant:reservation_list')
        # Si crea un admin o mesero, lo mandamos al dashboard
        return reverse_lazy('restaurant:dashboard')

    def form_valid(self, form):
        # Guardamos usuario
        response = super().form_valid(form)
        # Lo logueamos automáticamente
        login(self.request, self.object)
        # Y lo redirigimos según su rol
        return redirect(self.get_success_url())


def logout_view(request):
    logout(request)
    return redirect('accounts:login')
