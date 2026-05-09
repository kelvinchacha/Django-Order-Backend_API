from django.db import models
from django.conf import settings
from menu.models import Menu # Import Menu kutoka app yake mpya

# ==============================================================================
# MODEL: Order
# ROLE: Represents a customer order linked to a specific waiter and menu item.
# ARCHITECTURE: N-Tier with Foreign Key Integrity (Menu + User).
# ==============================================================================
class Order(models.Model):
    # Status Choices for strict validation and Admin control
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('cooking', 'Cooking'),
        ('ready', 'Ready'),
        ('served', 'Served'),
        ('cancelled', 'Cancelled'),
    ]

    # Linking to the waiter (User) - Data Isolation Layer
    waiter = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='my_orders'
    )
    
    # RELATIONAL INTEGRITY: Linking to the Menu Item instead of a string
    # PROTECT ensures we don't delete menu items that have existing orders
    menu_item = models.ForeignKey(
        Menu, 
        on_delete=models.PROTECT, 
        related_name='orders'
    )
    
    table_number = models.CharField(max_length=20)
    
    # Adding Quantity: Essential for Business Information Systems
    quantity = models.PositiveIntegerField(default=1)
    
    # Default status is set to 'pending' as per server-first integrity
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # Oda mpya ziwe juu

    def __str__(self):
        # Professional English string representation including quantity
        return f"{self.quantity}x {self.menu_item.item_name} - Table {self.table_number}"