from rest_framework import serializers
from .models import Order
from menu.models import Menu

class OrderSerializer(serializers.ModelSerializer):
    """
    SERIALIZER: OrderSerializer
    ROLE: Converts Order model instances into JSON for the React Native frontend.
    INTEGRITY: Implements read-only fields for automated server-side assignment 
               and dynamic price calculation.
    """
    # 1. Display Fields (Read-Only kwa ajili ya Frontend)
    # Tunavuta jina la chakula na jina la waiter kitalaamu
    menu_item_name = serializers.ReadOnlyField(source='menu_item.item_name')
    waiter_name = serializers.ReadOnlyField(source='waiter.full_name')
    
    # 2. Logic ya Bei: Price * Quantity
    # Hii inatusaidia kuonyesha jumla ya gharama ya oda hiyo moja kwa moja
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'waiter', 'waiter_name', 'menu_item', 'menu_item_name', 
            'table_number', 'quantity', 'total_price', 'status', 'created_at'
        ]
        
        # Security: Prevent the mobile app from manually setting protected fields
        read_only_fields = ['id', 'waiter', 'created_at']

    def get_total_price(self, obj):
        """
        Calculates the total cost for this order item.
        Formula: Price of Item (from Menu) * Quantity Ordered.
        """
        return obj.menu_item.price * obj.quantity

    def create(self, validated_data):
        """
        SERVER-FIRST INTEGRITY: Automatically assign the waiter from the request token.
        """
        # Tunatumia request user aliyelogin (JWT) kama waiter wa hii oda
        validated_data['waiter'] = self.context['request'].user
        return super().create(validated_data)