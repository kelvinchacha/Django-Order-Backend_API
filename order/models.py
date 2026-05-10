"""
Module: order.models
Description: The Core Transaction Engine. Handles multi-seat orders, 
             kitchen workflows, and financial state tracking.
Architect: Kelvin Chacha
"""

from django.db import models
from django.conf import settings
from menu.models import Menu

class Order(models.Model):
    """
    Represents a specific transaction item. 
    Redesigned to support granular seat tracking (A, B, C, D) 
    and dual-status monitoring (Kitchen vs Payment).
    """

    # --- Kitchen Workflow Status ---
    KITCHEN_STATUS = [
        ('pending', 'Pending (New)'),
        ('cooking', 'Cooking'),
        ('ready', 'Ready to Serve'),
        ('served', 'Served'),
        ('cancelled', 'Cancelled'),
    ]

    # --- Financial Integrity Status ---
    PAYMENT_STATUS = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    ]

    # --- Relational Integrity Layer ---
    waiter = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='managed_orders',
        db_index=True
    )
    
    menu_item = models.ForeignKey(
        Menu, 
        on_delete=models.PROTECT, 
        related_name='order_entries'
    )

    # --- Location Logic (The "One-Seat-One-Bill" Rule) ---
    table_number = models.CharField(max_length=10, db_index=True)
    seat_label = models.CharField(
        max_length=5, 
        default='A', 
        help_text="Seat identifier (e.g., A, B, C, D) for split billing."
    )

    quantity = models.PositiveIntegerField(default=1)
    
    # --- Financial Guard (Calculated on Server) ---
    # We store this to lock the price at the time of order, 
    # even if menu price changes later.
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    # --- Dual-Status Architecture ---
    kitchen_status = models.CharField(max_length=20, choices=KITCHEN_STATUS, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Order Transaction"
        verbose_name_plural = "Order Transactions"

    def save(self, *args, **kwargs):
        """
        SERVER-FIRST INTEGRITY RULE:
        Calculating prices on the server to prevent client-side manipulation.
        """
        if not self.pk: # Only on creation
            self.unit_price = self.menu_item.price
        
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"T{self.table_number}{self.seat_label} | {self.quantity}x {self.menu_item.item_name}"