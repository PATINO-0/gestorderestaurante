from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('WAITER', 'Mesero'),
        ('CUSTOMER', 'Cliente'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CUSTOMER')

    def is_admin(self):
        return self.role == 'ADMIN'

    def is_waiter(self):
        return self.role == 'WAITER'

    def is_customer(self):
        return self.role == 'CUSTOMER'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
