"""
Module: payments.serializers
Description: Financial settlement logic. 
             Handles multi-order reconciliation and automated status updates.
Architect: Kelvin Chacha
"""

from rest_framework import serializers
from django.db import transaction
from .models import Payment
from order.models import Order

class PaymentSerializer(serializers.ModelSerializer):
    """
    Handles complex payment processing.
    Implements Atomic Transactions to ensure Order and Payment states stay synced.
    """
    
    class Meta:
        model = Payment
        fields = [
            'id', 
            'orders', 
            'total_amount', 
            'amount_received', 
            'change_given', 
            'payment_method', 
            'transaction_id', 
            'paid_at'
        ]
        read_only_fields = ['id', 'total_amount', 'change_given', 'paid_at']

    def validate(self, data):
        """
        SERVER-FIRST INTEGRITY:
        Calculate the required total amount by summing up the linked orders.
        """
        orders = data.get('orders')
        if not orders:
            raise serializers.ValidationError("At least one order must be selected for payment.")
        
        # Checking if any order is already paid
        for order in orders:
            if order.payment_status == 'paid':
                raise serializers.ValidationError(f"Order #{order.id} has already been settled.")

        # Summing up total_price from the Order model
        calculated_total = sum(order.total_price for order in orders)
        data['total_amount'] = calculated_total
        
        return data

    @transaction.atomic
    def create(self, validated_data):
        """
        ATOMIC OPERATION:
        1. Create the Payment record.
        2. Bulk update all associated Orders to 'paid'.
        """
        orders = validated_data.pop('orders')
        payment = Payment.objects.create(**validated_data)
        payment.orders.set(orders)
        
        # High-Speed Update: Switch payment_status for all orders at once
        Order.objects.filter(id__in=[o.id for o in orders]).update(payment_status='paid')
        
        return payment