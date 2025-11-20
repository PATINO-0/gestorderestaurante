from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from restaurant.models import Dish
from restaurant.forms import DishForm
from restaurant.permissions import RoleRequiredMixin


class DishListView(RoleRequiredMixin, ListView):
    model = Dish
    template_name = 'restaurant/dish_list.html'
    context_object_name = 'dishes'
    allowed_roles = ['ADMIN', 'WAITER']


class DishCreateView(RoleRequiredMixin, CreateView):
    model = Dish
    form_class = DishForm
    template_name = 'restaurant/dish_form.html'
    success_url = reverse_lazy('restaurant:dish_list')
    allowed_roles = ['ADMIN', 'WAITER']


class DishUpdateView(RoleRequiredMixin, UpdateView):
    model = Dish
    form_class = DishForm
    template_name = 'restaurant/dish_form.html'
    success_url = reverse_lazy('restaurant:dish_list')
    allowed_roles = ['ADMIN', 'WAITER']


class DishDeleteView(RoleRequiredMixin, DeleteView):
    model = Dish
    template_name = 'restaurant/dish_confirm_delete.html'
    success_url = reverse_lazy('restaurant:dish_list')
    allowed_roles = ['ADMIN', 'WAITER' ]
