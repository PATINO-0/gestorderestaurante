from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings

from restaurant.models import Order, OrderItem
from restaurant.forms import OrderForm, OrderItemForm
from restaurant.permissions import RoleRequiredMixin


OrderItemFormSet = inlineformset_factory(
    Order, OrderItem, form=OrderItemForm, extra=1, can_delete=True
)


class OrderListView(RoleRequiredMixin, ListView):
    model = Order
    template_name = 'restaurant/order_list.html'
    context_object_name = 'orders'
    allowed_roles = ['ADMIN', 'WAITER', 'CUSTOMER']

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.role == 'CUSTOMER':
            qs = qs.filter(customer=user)
        return qs


class OrderCreateView(RoleRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'restaurant/order_form.html'
    success_url = reverse_lazy('restaurant:order_list')
    allowed_roles = ['ADMIN', 'WAITER', 'CUSTOMER']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['items_formset'] = OrderItemFormSet(self.request.POST)
        else:
            context['items_formset'] = OrderItemFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context['items_formset']
        form.instance.customer = self.request.user
        if form.is_valid() and items_formset.is_valid():
            self.object = form.save()
            items_formset.instance = self.object
            items_formset.save()
            self.object.recalculate_total()
            self._send_order_email(self.object)
            return redirect(self.get_success_url())
        return self.form_invalid(form)

    def _send_order_email(self, order: Order):
        if order.customer and order.customer.email:
            subject = f"Confirmación de pedido #{order.id}"
            message = (
                f"Hola {order.customer.username},\n\n"
                f"Tu pedido #{order.id} ha sido registrado.\n"
                f"Mesa: {order.table.number}\n"
                f"Total: ${order.total_amount}\n\n"
                "¡Gracias por tu compra!"
            )
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.customer.email])


class OrderUpdateView(RoleRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'restaurant/order_form.html'
    success_url = reverse_lazy('restaurant:order_list')
    allowed_roles = ['ADMIN', 'WAITER']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['items_formset'] = OrderItemFormSet(self.request.POST, instance=self.object)
        else:
            context['items_formset'] = OrderItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context['items_formset']
        if form.is_valid() and items_formset.is_valid():
            self.object = form.save()
            items_formset.instance = self.object
            items_formset.save()
            self.object.recalculate_total()
            return redirect(self.get_success_url())
        return self.form_invalid(form)


class OrderDeleteView(RoleRequiredMixin, DeleteView):
    model = Order
    template_name = 'restaurant/order_confirm_delete.html'
    success_url = reverse_lazy('restaurant:order_list')
    # 🔹 Mesero también puede eliminar pedidos
    allowed_roles = ['ADMIN', 'WAITER']
