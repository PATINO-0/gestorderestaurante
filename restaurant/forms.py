from datetime import date

from django import forms
from .models import Dish, Ingredient, Table, Reservation, Order, OrderItem


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'price', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'unit', 'stock_quantity', 'min_stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'min_stock': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['number', 'capacity', 'is_active']
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'date', 'time', 'guests']
        widgets = {
            'table': forms.Select(attrs={'class': 'form-select'}),
            # Date picker HTML5
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),
            # Time picker HTML5
            'time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                }
            ),
            'guests': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '1',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Solo mesas activas
        self.fields['table'].queryset = Table.objects.filter(is_active=True)

        # No permitir fechas pasadas
        self.fields['date'].widget.attrs['min'] = date.today().isoformat()

        if user is not None and hasattr(user, 'role') and user.role == 'CUSTOMER':
            self.fields['table'].label = "Mesa disponible"
            self.fields['guests'].label = "Número de personas"


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['dish', 'quantity']
        widgets = {
            'dish': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # 🔹 Incluimos status para que admin/mesero lo modifiquen
        fields = ['table', 'status']
        widgets = {
            'table': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        # recibimos el usuario desde la vista
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Si es cliente, ocultamos el campo status y lo fijamos a PENDING
        if user is not None and hasattr(user, 'role') and user.role == 'CUSTOMER':
            self.fields['status'].widget = forms.HiddenInput()
            if not self.instance.pk:
                # solo en creación, por si acaso
                self.fields['status'].initial = 'PENDING'
