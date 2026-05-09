from rest_framework import generics, permissions, status # Hapa ndipo tulipoimarisha
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone

from .models import Payment
from .serializers import PaymentSerializer
from order.models import Order

# ==============================================================================
# VIEW: PaymentCreate
# ROLE: Handles payment processing and order status transition.
# ==============================================================================
class PaymentCreate(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save()
        # Server-First Integrity: Update Order to 'paid'
        order = payment.order
        order.status = 'paid'
        order.save()

# ==============================================================================
# VIEW: DailySummaryView
# ROLE: Financial auditing for managers (EOD Report).
# ==============================================================================
class DailySummaryView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        today = timezone.now().date()
        
        summary = Payment.objects.filter(paid_at__date=today).values('payment_method').annotate(
            total_amount=Sum('amount_paid')
        )

        grand_total = Payment.objects.filter(paid_at__date=today).aggregate(
            total=Sum('amount_paid')
        )['total'] or 0

        return Response({
            "date": today,
            "summary_by_method": list(summary),
            "grand_total": grand_total,
            "currency": "TZS"
        }, status=status.HTTP_200_OK)