"""
Module: users.serializers
Description: Data transformation layer for User Identity.
             Integrates with aXeraf Technologies Security Standards.
Architect: Kelvin Chacha
"""

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializes the User model for safe delivery to the frontend.
    Strictly excludes sensitive fields and enforces read-only business logic.
    """
    
    # Adding human-readable role name for the UI (Layer 1)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 
            'phone_number', 
            'username', 
            'role', 
            'role_display', 
            'is_default_password',
            'is_active'
        ]
        
        # Security Guard: These fields should not be changed by the user via this serializer
        read_only_fields = ['role', 'phone_number']

    def validate_phone_number(self, value):
        """
        Business Logic: Ensure the phone number follows a specific format if needed.
        """
        if len(value) < 10:
            raise serializers.ValidationError("Phone number must be at least 10 digits.")
        return value