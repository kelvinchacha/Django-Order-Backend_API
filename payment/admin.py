"""
Module: payments.admin
Description: Financial Audit Dashboard. 
             Enforces strict immutability on payment records for audit trails.
Architect: Kelvin Chacha
"""
from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Architectural customization for financial monitoring.
    Designed to prevent internal fraud and enable easy transaction tracking.
    """

    # Grid View: Crucial for daily cash reconciliation
    list_display = (
        'id', 
        'payment_method', 
        'total_amount', 
        'amount_received', 
        'change_given', 
        'transaction_id', 
        'paid_at'
    )

    # Filters: Enable Managers to audit specific payment providers
    list_filter = ('payment_method', 'paid_at')

    # Search: Rapid retrieval using Mobile Money Reference IDs
    search_fields = ('transaction_id', 'orders__table_number')

    # Security: Payment records must be Read-Only after creation
    # This prevents anyone from changing "Amount Paid" later.
    readonly_fields = (
        'orders', 
        'total_amount', 
        'amount_received', 
        'change_given', 
        'payment_method', 
        'transaction_id', 
        'paid_at'
    )

    # UI Organization: Grouping transaction data
    fieldsets = (
        ('Settlement Details', {
            'fields': ('payment_method', 'transaction_id', 'paid_at')
        }),
        ('Financial Breakdown', {
            'fields': ('total_amount', 'amount_received', 'change_given')
        }),
        ('Linked Orders', {
            'fields': ('orders',),
            'description': 'List of specific menu items settled in this transaction.'
        }),
    )

    def has_add_permission(self, request):
        """
        Security: Payments should generally be created via the API (App).
        Manual creation in Admin is disabled to enforce the Business Logic Chain.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Financial Integrity: Deleting payment records is strictly prohibited
        to maintain a permanent audit trail.
        """
        return False