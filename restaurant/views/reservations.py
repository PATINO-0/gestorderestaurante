from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.timezone import now

from restaurant.models import Reservation
from restaurant.forms import ReservationForm
from restaurant.permissions import RoleRequiredMixin
from accounts.models import User


class ReservationListView(RoleRequiredMixin, ListView):
    model = Reservation
    template_name = 'restaurant/reservation_list.html'
    context_object_name = 'reservations'
    allowed_roles = ['ADMIN', 'WAITER', 'CUSTOMER']

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == 'CUSTOMER':
            qs = qs.filter(customer=user)
        return qs


class ReservationCreateView(RoleRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'restaurant/reservation_form.html'
    success_url = reverse_lazy('restaurant:reservation_list')
    allowed_roles = ['ADMIN', 'WAITER', 'CUSTOMER']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.customer = self.request.user
        # Aquí se respeta la restricción de mesa única por fecha/hora
        return super().form_valid(form)


class ReservationUpdateView(RoleRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'restaurant/reservation_form.html'
    success_url = reverse_lazy('restaurant:reservation_list')
    allowed_roles = ['ADMIN', 'WAITER', 'CUSTOMER']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.role == 'CUSTOMER':
            qs = qs.filter(customer=user)
        return qs


class ReservationDeleteView(RoleRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'restaurant/reservation_confirm_delete.html'
    success_url = reverse_lazy('restaurant:reservation_list')
    allowed_roles = ['ADMIN', 'WAITER', 'CUSTOMER']

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.role == 'CUSTOMER':
            qs = qs.filter(customer=user)
        return qs
