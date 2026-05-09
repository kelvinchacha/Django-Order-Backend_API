from django.db import models
from order.models import Order

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('mobile_money', 'Mobile Money (Tigo/M-Pesa)'),
        ('n_card', 'N-Card'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment_record')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    transaction_id = models.CharField(max_length=100, blank=True, null=True) # Kwa miamala ya simu
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.amount_paid} TZS"