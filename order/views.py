"""
Module: order.views
Description: Identity-Aware Transaction Controller. 
             Optimized for Kitchen Workflows and Granular Billing.
Architect: Kelvin Chacha
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum

from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """
    A professional ViewSet for handling the Order Lifecycle.
    - Waiters: View and manage their own table assignments.
    - Chefs: View all pending kitchen tickets regardless of waiter.
    - Managers: Audit all financial transactions.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        DATA ISOLATION LAYER (IAM Integration):
        Logic: Filters orders based on the operational role of the requester.
        """
        user = self.request.user
        queryset = Order.objects.select_related('menu_item', 'waiter')

        # 1. ADMIN/MANAGER: Total Visibility
        if user.role in ['ADMIN', 'MANAGER']:
            return queryset

        # 2. CHEF: Kitchen Visibility (Sees all items that need cooking)
        if user.role == 'CHEF':
            return queryset.filter(kitchen_status__in=['pending', 'cooking'])

        # 3. WAITER: Service Visibility (Sees their own assigned orders only)
        return queryset.filter(waiter=user)

    @action(detail=False, methods=['get'])
    def bill_summary(self, request):
        """
        FINANCIAL LOGIC: Supports Split-Billing (by Table or by Seat).
        Usage: /api/order/orders/bill_summary/?table=5&seat=A
        """
        table = request.query_params.get('table')
        seat = request.query_params.get('seat') # Optional seat parameter

        if not table:
            return Response({"detail": "Table number is required."}, status=400)

        filters = {'table_number': table, 'payment_status': 'unpaid'}
        if seat:
            filters['seat_label'] = seat

        orders = Order.objects.filter(**filters)
        total = orders.aggregate(total=Sum('total_price'))['total'] or 0

        return Response({
            "table": table,
            "seat": seat if seat else "All Seats",
            "total_amount": total,
            "item_count": orders.count()
        })

    def perform_create(self, serializer):
        """
        SERVER-FIRST INTEGRITY:
        Automatic assignment of the 'waiter' from the authenticated context.
        """
        serializer.save(waiter=self.request.user)