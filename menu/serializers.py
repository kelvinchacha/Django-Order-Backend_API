from rest_framework import serializers
from .models import Menu

class MenuSerializer(serializers.ModelSerializer):
    """
    Business Logic: Handles transformation of Menu data into JSON.
    Standard: aXeraf Technologies Data Formatting.
    """
    class Meta:
        model = Menu
        fields = ['id', 'item_name', 'price', 'status', 'description', 'created_at']