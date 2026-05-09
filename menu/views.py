from rest_framework import viewsets, permissions
from .models import Menu
from .serializers import MenuSerializer

class MenuViewSet(viewsets.ModelViewSet):
    """
    SECURITY ARCHITECTURE:
    - Admin (Staff): Full CRUD capability (Create, Update, Delete).
    - Waiter (Authenticated): Read-Only access to see what's available.
    - Anonymous: Blocked (401 Unauthorized).
    """
    queryset = Menu.objects.all().order_by('item_name')
    serializer_class = MenuSerializer

    def get_permissions(self):
        # 1. SAFES METHODS (GET, HEAD, OPTIONS)
        # Waiters can check the menu to take orders.
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        
        # 2. DESTRUCTIVE METHODS (POST, PUT, PATCH, DELETE)
        # Only Admins/Staff can change prices or add menu items.
        return [permissions.IsAdminUser()]