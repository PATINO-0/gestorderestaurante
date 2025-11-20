from django.db import models
from django.conf import settings
from .table import Table


class Reservation(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pendiente'),
        ('CONFIRMED', 'Confirmada'),
        ('CANCELLED', 'Cancelada'),
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    table = models.ForeignKey(Table, on_delete=models.PROTECT, related_name='reservations')
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-time']
        unique_together = ('table', 'date', 'time')

    def __str__(self):
        return f"Reserva de {self.customer} - Mesa {self.table.number} - {self.date} {self.time}"
