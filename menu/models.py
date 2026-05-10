"""
Module: menu.models
Description: Menu management logic for aXeraf Technologies.
             Supports categorization and real-time availability tracking.
Architect: Kelvin Chacha
"""

from django.db import models

class Menu(models.Model):
    """
    Represents a product or service offered in the system.
    Integrated with Chef's kitchen monitor for status updates.
    """
    
    # --- Category Definitions ---
    # Helps in Layer 1 (UI) filtering and Layer 3 (State) management
    CATEGORY_CHOICES = [
        ('FOOD', 'Food'),
        ('DRINK', 'Drinks'),
        ('SNACK', 'Snacks/Starters'),
        ('OTHER', 'Other Services'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('out_of_stock', 'Out of Stock'),
        ('wait', 'Wait (Preparation Needed)'),
    ]

    # --- Core Fields ---
    item_name = models.CharField(
        max_length=100, 
        unique=True, 
        db_index=True # Indexed for fast search in UI
    )
    
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default='FOOD'
    )
    
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Price in TZS"
    ) 
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='available'
    )
    
    description = models.TextField(
        blank=True, 
        null=True,
        help_text="Ingredients or extra details"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # Track when Chef changed status

    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
        ordering = ['category', 'item_name']

    def __str__(self):
        """Returns string representation for Admin and Dropdowns."""
        return f"{self.item_name} ({self.get_category_display()}) - {self.price} TZS"