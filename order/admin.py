from django.contrib import admin
from .models import Order

# ==============================================================================
# ADMIN CONFIGURATION: OrderAdmin
# ROLE: Provides a professional interface for managing orders.
# ARCHITECTURE: Part of the Internal Management Layer for aXeraf Technologies.
# ==============================================================================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # REFACTORED: We use 'menu_item' instead of the deleted 'food_item'
    list_display = ('id', 'menu_item', 'table_number', 'waiter', 'status', 'created_at')
    
    # Professional filtering options for business reporting and auditing
    list_filter = ('status', 'waiter', 'created_at')
    
    # SEARCH LOGIC: Using double underscore (__) to search the Menu Table's name field
    search_fields = ('menu_item__item_name', 'table_number', 'waiter__username')
    
    # Default ordering to show the most recent orders first (Reverse Chronological)
    ordering = ('-created_at',)

    # Ensuring financial integrity by making timestamp read-only
    readonly_fields = ('created_at',)