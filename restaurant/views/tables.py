from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from restaurant.models import Table
from restaurant.forms import TableForm
from restaurant.permissions import RoleRequiredMixin


class TableListView(RoleRequiredMixin, ListView):
    model = Table
    template_name = 'restaurant/table_list.html'
    context_object_name = 'tables'
    allowed_roles = ['ADMIN', 'WAITER']


class TableCreateView(RoleRequiredMixin, CreateView):
    model = Table
    form_class = TableForm
    template_name = 'restaurant/table_form.html'
    success_url = reverse_lazy('restaurant:table_list')
    allowed_roles = ['ADMIN']


class TableUpdateView(RoleRequiredMixin, UpdateView):
    model = Table
    form_class = TableForm
    template_name = 'restaurant/table_form.html'
    success_url = reverse_lazy('restaurant:table_list')
    allowed_roles = ['ADMIN']


class TableDeleteView(RoleRequiredMixin, DeleteView):
    model = Table
    template_name = 'restaurant/table_confirm_delete.html'
    success_url = reverse_lazy('restaurant:table_list')
    allowed_roles = ['ADMIN']
