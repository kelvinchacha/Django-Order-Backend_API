from rest_framework import serializers
from .models import Order  # Updated from Oda to Order

# ==============================================================================
# SERIALIZER: OrderSerializer
# ROLE: Converts Order model instances into JSON for the React Native frontend.
# INTEGRITY: Implements read-only fields for automated server-side assignment.
# ==============================================================================
class OrderSerializer(serializers.ModelSerializer):
    # We make waiter read_only so it's not required in the POST request body.
    # The server will handle this assignment automatically in the View.
    waiter_name = serializers.ReadOnlyField(source='waiter.username')

    class Meta:
        model = Order
        fields = ['id', 'waiter', 'waiter_name', 'table_number', 'food_item', 'status', 'created_at']
        
        # Security: Prevent the mobile app from manually setting the waiter
        extra_kwargs = {
            'waiter': {'read_only': True}
        }