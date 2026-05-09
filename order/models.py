from django.db import models
from django.conf import settings

# ==============================================================================
# MODEL: Order
# ROLE: Represents a customer order in the system.
# RELATIONSHIP: Linked to the User model (Waiter) for Data Isolation.
# ==============================================================================
class Order(models.Model):
    # Status Choices for strict validation and Admin dropdown
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('cooking', 'Cooking'),
        ('ready', 'Ready'),
        ('served', 'Served'),
        ('cancelled', 'Cancelled'),
    ]

    # Linking the order to the specific waiter who created it
    waiter = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='my_orders'
    )
    
    table_number = models.CharField(max_length=20)
    food_item = models.CharField(max_length=100)
    
    # Default status is set to 'pending' as per business logic
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Professional English string representation
        return f"{self.food_item} - Table {self.table_number} ({self.status})"