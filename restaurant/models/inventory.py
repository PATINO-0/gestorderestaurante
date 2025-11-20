from django.db import models
from .ingredient import Ingredient


class InventoryMovement(models.Model):
    MOVEMENT_TYPE = (
        ('IN', 'Entrada'),
        ('OUT', 'Salida'),
    )

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_movement_type_display()} {self.ingredient.name} ({self.quantity})"
