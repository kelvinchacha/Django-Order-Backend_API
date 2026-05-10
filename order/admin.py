"""
Module: order.admin
Description: High-level Audit and Transaction Monitoring.
             Designed for Financial Integrity and Kitchen Workflow Oversight.
Architect: Kelvin Chacha
"""
from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Architectural customization of the Order Admin interface.
    Focuses on dual-status tracking and financial auditing.
    """
    
    # Grid View: Adding seat_label, prices, and dual statuses
    list_display = (
        'id', 
        'table_reference', 
        'menu_item', 
        'quantity', 
        'total_price', 
        'kitchen_status', 
        'payment_status', 
        'waiter', 
        'created_at'
    )
    
    # Audit Filters: Crucial for Managerial Reporting
    list_filter = (
        'payment_status', 
        'kitchen_status', 
        'waiter', 
        'table_number', 
        'created_at'
    )
    
    # Deep Search: Across related models
    search_fields = (
        'table_number', 
        'menu_item__item_name', 
        'waiter__username', 
        'waiter__phone_number'
    )
    
    # Management Actions: Allows Manager to mark multiple items as Paid quickly
    list_editable = ('kitchen_status', 'payment_status')
    
    # Security: Financial data must remain immutable in the Admin panel
    readonly_fields = ('unit_price', 'total_price', 'created_at', 'updated_at')

    # Custom Field for Cleaner UI
    def table_reference(self, obj):
        """Combines Table Number and Seat Label for easier identification."""
        return f"T-{obj.table_number} [Seat {obj.seat_label}]"
    table_reference.short_description = 'Location'

    fieldsets = (
        ('Transaction Identity', {
            'fields': ('waiter', 'menu_item', 'quantity')
        }),
        ('Location Details', {
            'fields': ('table_number', 'seat_label')
        }),
        ('Workflow & Financial Status', {
            'fields': ('kitchen_status', 'payment_status')
        }),
        ('Audit Logs (Read-Only)', {
            'fields': ('unit_price', 'total_price', 'created_at', 'updated_at'),
            'classes': ('collapse',), # Hides sensitive audit data by default
        }),
    )