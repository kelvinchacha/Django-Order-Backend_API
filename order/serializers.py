"""
Module: order.serializers
Description: High-integrity data transformation for transactions.
             Supports dual-status tracking and split-billing identification.
Architect: Kelvin Chacha
"""

from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    """
    Converts Order instances to JSON for React Native.
    Enforces Server-First Integrity by locking prices and auto-assigning waiters.
    """
    # 1. Human-Readable Display Fields (Read-Only)
    # These help the UI display details without extra API calls
    menu_item_name = serializers.ReadOnlyField(source='menu_item.item_name')
    waiter_name = serializers.ReadOnlyField(source='waiter.username')
    kitchen_status_display = serializers.CharField(source='get_kitchen_status_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 
            'waiter', 
            'waiter_name', 
            'menu_item', 
            'menu_item_name', 
            'table_number', 
            'seat_label', 
            'quantity', 
            'unit_price', # Locked price at time of order
            'total_price', 
            'kitchen_status', 
            'kitchen_status_display',
            'payment_status', 
            'payment_status_display',
            'created_at'
        ]
        
        # Security Guard: Financial and ownership fields are managed by the Server
        read_only_fields = [
            'id', 
            'waiter', 
            'unit_price', 
            'total_price', 
            'created_at'
        ]

    def create(self, validated_data):
        """
        SERVER-FIRST INTEGRITY: 
        Automatically binds the current authenticated user as the waiter.
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['waiter'] = request.user
        return super().create(validated_data)