from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

# Custom User Manager to handle filtering based on active users and roles
class CustomUserManager(UserManager):
    def get_queryset(self):
        # Only return active users
        return super().get_queryset().filter(is_active=True)

    def get_admin_users(self):
        # Retrieve users with the 'Admin' role
        return self.get_queryset().filter(role='Admin')

    def get_manager_users(self):
        # Retrieve users with the 'Manager' role
        return self.get_queryset().filter(role='Manager')

    def get_staff_users(self):
        # Retrieve users with the 'Staff' role
        return self.get_queryset().filter(role='Staff')


# Custom User model extending AbstractUser to include 'role' field
class User(AbstractUser):
    # Define possible roles for users in the system
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Staff', 'Staff'),
    ]
    
    # Role field for the user, default is 'Staff'
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Staff')

    # Use the custom manager to filter users by their role
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        # If the user is a superuser, automatically set their role to 'Admin'
        if self.is_superuser:
            self.role = 'Admin'
        super().save(*args, **kwargs)


# Inventory model to track items in the system
class Inventory(models.Model):
    # Item name, maximum length of 100 characters
    name = models.CharField(max_length=100)
    
    # Quantity of the item, must be a positive integer
    quantity = models.PositiveIntegerField()
    
    # Section to categorize items, maximum length of 50 characters
    section = models.CharField(max_length=50)
    
    # Link to the user who last updated the item; can be null
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        # Return the name of the inventory item as a string representation
        return self.name
