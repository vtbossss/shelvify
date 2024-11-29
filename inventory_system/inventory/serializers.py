# inventory/serializers.py
from rest_framework import serializers
from .models import User, Inventory

# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Fields to be serialized from the User model
        fields = ['id', 'username', 'email', 'role']

# Serializer for Inventory model
class InventorySerializer(serializers.ModelSerializer):
    # Represent the 'updated_by' field as a string (e.g., username)
    updated_by = serializers.StringRelatedField()

    class Meta:
        model = Inventory
        # Fields to be serialized from the Inventory model
        fields = ['id', 'name', 'quantity', 'section', 'updated_by']
