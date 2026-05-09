"""
Module: users.serializers
Description: Handles conversion of User models to JSON format for API 
             authentication and profile management.
"""

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializes the User model for safe delivery to the frontend.
    Excluded sensitive fields like raw passwords for security.
    """
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'username', 'role', 'is_default_password']
        # 'role' na 'is_default_password' ni muhimu kwa React Native Logic
