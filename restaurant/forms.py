from django import forms
from .models import Dish, Ingredient, Table, Reservation, Order, OrderItem
from accounts.models import User


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'price', 'is_active']


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'unit', 'stock_quantity', 'min_stock']


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['number', 'capacity', 'is_active']


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'date', 'time', 'guests']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Aquí podrías filtrar mesas activas o aplicar lógica extra


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['dish', 'quantity']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table']
