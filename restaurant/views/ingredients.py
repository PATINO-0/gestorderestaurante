from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from restaurant.models import Ingredient
from restaurant.forms import IngredientForm
from restaurant.permissions import RoleRequiredMixin


class IngredientListView(RoleRequiredMixin, ListView):
    model = Ingredient
    template_name = 'restaurant/ingredient_list.html'
    context_object_name = 'ingredients'
    allowed_roles = ['ADMIN', 'WAITER']


class IngredientCreateView(RoleRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'restaurant/ingredient_form.html'
    success_url = reverse_lazy('restaurant:ingredient_list')
    allowed_roles = ['ADMIN', 'WAITER']


class IngredientUpdateView(RoleRequiredMixin, UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'restaurant/ingredient_form.html'
    success_url = reverse_lazy('restaurant:ingredient_list')
    allowed_roles = ['ADMIN', 'WAITER']


class IngredientDeleteView(RoleRequiredMixin, DeleteView):
    model = Ingredient
    template_name = 'restaurant/ingredient_confirm_delete.html'
    success_url = reverse_lazy('restaurant:ingredient_list')
    allowed_roles = ['ADMIN', 'WAITER']
