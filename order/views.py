from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, F

from .models import Order
from .serializers import OrderSerializer

# ==============================================================================
# VIEWSET: OrderViewSet
# ROLE: High-level controller for managing the Order Lifecycle.
# ARCHITECTURE: Implements the N-Tier Service Layer for aXeraf Technologies.
# SECURITY: JWT-based Authentication with strict Row-Level Data Isolation.
# ==============================================================================
class OrderViewSet(viewsets.ModelViewSet):
    """
    A professional ViewSet for handling Order transactions.
    - Waiters: Can only view and manage their own assigned orders.
    - Managers: Have visibility over all system orders for financial auditing.
    """
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    # Advanced Filtering and Search capabilities
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'table_number']
    search_fields = ['menu_item__item_name', 'table_number']
    ordering_fields = ['created_at', 'status']

    # --------------------------------------------------------------------------
    # DATA ISOLATION LOGIC
    # --------------------------------------------------------------------------
    def get_queryset(self):
        """
        Retrieves the queryset based on user role.
        1. Staff/Admin: Can view all orders in the system.
        2. Waiter: Limited to orders where waiter_id == current_user_id.
        """
        user = self.request.user
        
        # Optimization: select_related reduces database hits for Menu data
        base_queryset = Order.objects.select_related('menu_item', 'waiter').order_by('-created_at')

        if user.is_staff:
            return base_queryset
        
        # Row-level security for regular waiters
        return base_queryset.filter(waiter=user)

    # --------------------------------------------------------------------------
    # SERVER-FIRST INTEGRITY RULE
    # --------------------------------------------------------------------------
    def perform_create(self, serializer):
        """
        Ensures the 'waiter' field is automatically populated from the JWT token.
        This prevents unauthorized waiters from creating orders on behalf of others.
        """
        serializer.save(waiter=self.request.user)

    # --------------------------------------------------------------------------
    # FINANCIAL LOGIC: Table Bill Calculation
    # --------------------------------------------------------------------------
    def get_table_total(self, table_number):
        """
        Calculates the outstanding balance for a specific table.
        Logic: Sum of (Menu Price * Quantity) for all 'unpaid' orders.
        """
        return Order.objects.filter(
            table_number=table_number
        ).exclude(
            status__in=['cancelled', 'paid']
        ).aggregate(
            total=Sum(F('menu_item__price') * F('quantity'))
        )['total'] or 0