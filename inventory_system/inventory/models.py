# inventory/models.py
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class CustomUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)  # Filter for active users

    def get_admin_users(self):
        return self.get_queryset().filter(role='Admin')

    def get_manager_users(self):
        return self.get_queryset().filter(role='Manager')

    def get_staff_users(self):
        return self.get_queryset().filter(role='Staff')


class User(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Staff', 'Staff'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Staff')

    # Set default manager
    objects = CustomUserManager()

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