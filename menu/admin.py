"""
Module: menu.admin
Description: Advanced Admin panel configuration for Menu management.
             Optimized for real-time price updates and category filtering.
Architect: Kelvin Chacha
"""
from django.contrib import admin
from .models import Menu

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """
    Architectural customization of the Menu Admin interface.
    Enables rapid inventory management for Managers.
    """
    
    # Grid View: Adding 'category' and 'updated_at' for better monitoring
    list_display = (
        'item_name', 
        'category', 
        'price', 
        'status', 
        'updated_at'
    )
    
    # Audit Filters: Managers can now filter by Category and Status simultaneously
    list_filter = ('category', 'status', 'created_at')
    
    # Fast Search: Indexed search by item name
    search_fields = ('item_name',)
    
    # Live Editing: Allows on-the-fly updates for price and availability
    list_editable = ('price', 'status', 'category')
    
    # Layout Organization: Grouping fields inside the edit form
    fieldsets = (
        ('Basic Information', {
            'fields': ('item_name', 'category', 'description')
        }),
        ('Financial & Status', {
            'fields': ('price', 'status'),
            'description': 'Critical business data: ensure accuracy before saving.'
        }),
    )

    # Ordering by category then name for a cleaner list
    ordering = ('category', 'item_name')