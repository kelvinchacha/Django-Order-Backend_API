"""
Module: payments.views
Description: Revenue management and financial auditing controllers.
             Optimized for End-of-Day (EOD) reporting and real-time reconciliations.
Architect: Kelvin Chacha
"""

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count  # Import Count hapa kitalaamu
from django.utils import timezone

from .models import Payment
from .serializers import PaymentSerializer

class PaymentCreateView(generics.CreateAPIView):
    """
    Handles the creation of new payment records.
    Note: The 'paid' status update for Orders is now handled 
    within the Serializer's atomic transaction for better integrity.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

class RevenueDashboardView(APIView):
    """
    EXECUTIVE DASHBOARD:
    Provides a deep-dive into the day's financial performance.
    Only accessible by Managers and Admins.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        today = timezone.now().date()
        payments_today = Payment.objects.filter(paid_at__date=today)
        
        # 1. Break down by Payment Method
        # Tunatumia Count('id') moja kwa moja hapa
        method_summary = payments_today.values('payment_method').annotate(
            total_collected=Sum('total_amount'),
            transaction_count=Count('id')
        )

        # 2. Grand Totals (Actual Cash vs Expected Bill)
        totals = payments_today.aggregate(
            grand_total=Sum('total_amount'),
            total_received=Sum('amount_received'),
            total_change=Sum('change_given')
        )

        return Response({
            "audit_date": today,
            "performance_metrics": {
                "total_revenue": totals['grand_total'] or 0,
                "total_cash_handled": totals['total_received'] or 0,
                "total_change_issued": totals['total_change'] or 0,
                "transaction_volume": payments_today.count()
            },
            "breakdown": list(method_summary),
            "currency": "TZS",
            "status": "Finalized" if timezone.now().hour > 22 else "In-Progress"
        }, status=status.HTTP_200_OK)