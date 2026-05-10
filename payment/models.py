"""
Module: payments.models
Description: Financial Settlement Layer. Handles revenue collection,
             transaction tracking, and payment verification.
Architect: Kelvin Chacha
"""

from django.db import models
from order.models import Order
from django.core.exceptions import ValidationError

class Payment(models.Model):
    """
    Represents a financial transaction for one or more orders.
    Integrated with Mobile Money and N-Card validation logic.
    """
    
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('mpesa', 'Vodacom M-Pesa'),
        ('tigopesa', 'Tigo Pesa'),
        ('airtelmoney', 'Airtel Money'),
        ('n_card', 'N-Card'),
        ('halo_pesa', 'Halo Pesa'),
    ]

    # ARCHITECTURE CHANGE: 
    # Using ManyToMany allows one payment to settle multiple order items 
    # (e.g., settling the whole bill for Seat A at once).
    orders = models.ManyToManyField(
        Order, 
        related_name='payments',
        help_text="The orders being settled in this transaction."
    )
    
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Calculated total from linked orders."
    )
    
    amount_received = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Actual amount handed over by customer."
    )
    
    change_given = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00
    )

    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHODS, 
        default='cash'
    )
    
    transaction_id = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        unique=True,
        help_text="Reference ID for Mobile Money or N-Card."
    )
    
    paid_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Financial Transaction"
        verbose_name_plural = "Financial Transactions"
        ordering = ['-paid_at']

    def clean(self):
        """
        Business Logic: Ensure amount received is not less than the bill.
        """
        if self.amount_received < self.total_amount:
            raise ValidationError("Amount received cannot be less than the total bill.")

    def save(self, *args, **kwargs):
        """
        Automatic Calculation of Change.
        """
        self.change_given = self.amount_received - self.total_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"TXN-{self.id} | {self.total_amount} TZS via {self.get_payment_method_display()}""""
Module: payments.models
Description: Financial Settlement Layer. Handles revenue collection,
             transaction tracking, and payment verification.
Architect: Kelvin Chacha
"""