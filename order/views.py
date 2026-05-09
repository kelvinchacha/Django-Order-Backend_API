from rest_framework import generics, permissions, filters
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order
from .serializers import OrderSerializer

# ==============================================================================
# VIEW: OrderList
# RESPONSIBILITY: Handles listing and creation of order records.
# ARCHITECTURE: Part of the API/Service layer in the 5-Layer Communication Chain.
# SECURITY: Implements JWT Authentication and Row-Level Security (Data Isolation).
# FEATURES: Supports history tracking via date ordering and filtering.
# ==============================================================================
class OrderList(generics.ListCreateAPIView):
    """
    Concrete view for listing orders belonging to the authenticated waiter 
    and allowing the creation of new orders with automated waiter assignment.
    """
    serializer_class = OrderSerializer

    # ENFORCING STRICT AUTHENTICATION AND PERMISSION LAYERS
    # --------------------------------------------------------------------------
    # Mandatory login via JWT is enforced here.
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    # Adding support for filtering and searching in the history
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['food_item', 'table_number']

    # DATA ISOLATION & HISTORY LOGIC (VYUMBA NA MUDA)
    # --------------------------------------------------------------------------
    def get_queryset(self):
        """
        1. Isolation: Filters orders so waiters only see their own data.
        2. History: Orders the results by 'created_at' descending (Newest first).
        3. Dynamic Filtering: Allows filtering by specific date via query parameters.
        """
        user = self.request.user
        queryset = Order.objects.filter(waiter=user).order_by('-created_at')

        # Logic for filtering by date (e.g., /api/order/?date=2026-05-09)
        order_date = self.request.query_params.get('date')
        if order_date:
            queryset = queryset.filter(created_at__date=order_date)
            
        return queryset

    # SERVER-FIRST INTEGRITY RULE
    # --------------------------------------------------------------------------
    def perform_create(self, serializer):
        """
        Server-side validation: Automatically attaches the logged-in waiter 
        to the order. State is only confirmed after a successful 201 Created.
        """
        # Automatically set the 'waiter' to the current authenticated user.
        # 'status' defaults to 'pending' as defined in the Model.
        serializer.save(waiter=self.request.user)