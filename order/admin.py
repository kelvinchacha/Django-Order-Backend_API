from django.contrib import admin
from .models import Order  # Updated from Oda to Order to match global standards

# ==============================================================================
# ADMIN CONFIGURATION: OrderAdmin
# ROLE: Provides a professional interface for managing orders.
# FEATURES: List filtering, searching, and status management.
# ==============================================================================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Columns to be displayed in the Admin table
    list_display = ('id', 'food_item', 'table_number', 'waiter', 'status', 'created_at')
    
    # Professional filtering options for business reporting
    list_filter = ('status', 'waiter', 'created_at')
    
    # Search functionality to quickly find specific orders
    search_fields = ('food_item', 'table_number', 'waiter__username')
    
    # Default ordering to show the most recent orders first
    ordering = ('-created_at',)

    # Ensuring fields like 'created_at' are visible but not editable
    readonly_fields = ('created_at',)