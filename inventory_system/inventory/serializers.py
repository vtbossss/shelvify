# inventory/serializers.py
from rest_framework import serializers
from .models import User, Inventory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class InventorySerializer(serializers.ModelSerializer):
    updated_by = serializers.StringRelatedField()

    class Meta:
        model = Inventory
        fields = ['id', 'name', 'quantity', 'section', 'updated_by']
