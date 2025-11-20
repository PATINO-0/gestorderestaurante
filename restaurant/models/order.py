from django.db import models
from django.conf import settings
from .table import Table
from .dish import Dish


class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pendiente'),
        ('IN_PROGRESS', 'En preparación'),
        ('SERVED', 'Servida'),
        ('CANCELLED', 'Cancelada'),
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    table = models.ForeignKey(Table, on_delete=models.PROTECT, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Pedido #{self.id} - Mesa {self.table.number}"

    def recalculate_total(self):
        total = sum(item.line_total for item in self.items.all())
        self.total_amount = total
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey(Dish, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.unit_price = self.unit_price or self.dish.price
        self.line_total = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.dish.name} x {self.quantity}"
