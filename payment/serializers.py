from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    """
    Handles the transformation of payment data.
    Linked to a specific order to ensure financial integrity.
    """
    class Meta:
        model = Payment
        fields = ['id', 'order', 'amount_paid', 'payment_method', 'transaction_id', 'paid_at']
        read_only_fields = ['paid_at']
