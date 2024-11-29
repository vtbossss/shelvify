# inventory/permissions.py
from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Custom permission to allow access only to users with the 'Admin' role.
    This ensures that only admins can access specific resources or actions.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and has the 'Admin' role
        return request.user.is_authenticated and request.user.role == 'Admin'


class IsManager(BasePermission):
    """
    Custom permission to allow access only to users with the 'Manager' role.
    This ensures that managers can access resources specific to their role.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and has the 'Manager' role
        return request.user.is_authenticated and request.user.role == 'Manager'


class IsStaff(BasePermission):
    """
    Custom permission to allow access only to users with the 'Staff' role.
    This ensures that staff members can access resources designated for them.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and has the 'Staff' role
        return request.user.is_authenticated and request.user.role == 'Staff'
