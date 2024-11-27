# inventory/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Staff', 'Staff'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Staff')

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'Admin'  # Superuser is always Admin
        super().save(*args, **kwargs)


class Inventory(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    section = models.CharField(max_length=50)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name