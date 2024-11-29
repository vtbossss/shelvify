"""
URL configuration for inventory_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin URL route for Django's admin interface
    path("admin/", admin.site.urls),  # Route to access the Django admin panel

    # Include the URL patterns from the 'inventory' app
    path('', include('inventory.urls')),  # All routes defined in 'inventory.urls' will be included here
]
