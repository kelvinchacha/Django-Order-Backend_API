"""
Module: menu.serializers
Description: Business Logic for Menu Data Transformation.
             Supports multi-role UI states for Waiters and Chefs.
Standard: aXeraf Technologies Data Formatting.
Architect: Kelvin Chacha
"""

from rest_framework import serializers
from .models import Menu

class MenuSerializer(serializers.ModelSerializer):
    """
    Serializes Menu items with human-readable choices for the UI.
    Includes categorization for efficient Layer 1 filtering.
    """
    
    # Human-readable transformations for the React Native Frontend
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Menu
        fields = [
            'id', 
            'item_name', 
            'category', 
            'category_display', 
            'price', 
            'status', 
            'status_display', 
            'description', 
            'created_at'
        ]
        
    def validate_price(self, value):
        """
        Integrity Check: Ensure no item is listed with zero or negative price.
        """
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive value.")
        return value