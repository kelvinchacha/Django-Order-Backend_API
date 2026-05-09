from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Oda
from .serializers import OdaSerializer

# ==============================================================================
# VIEW: OdaList
# RESPONSIBILITY: Handles listing and creation of order records.
# ARCHITECTURE: Part of the API/Service layer in the 5-Layer Communication Chain.
# SECURITY: Implements JWT Authentication to ensure only authorized users 
#           can access business-sensitive data.
# ==============================================================================
class OdaList(generics.ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    The list is ordered by 'muda' (timestamp) in descending order to prioritize 
    recent activities.
    """
    
    # Fetching all order records and sorting by timestamp descending
    queryset = Oda.objects.all().order_by('-muda')
    
    # Mapping the model data to JSON format via OdaSerializer
    serializer_class = OdaSerializer

    # ENFORCING STRICT AUTHENTICATION AND PERMISSION LAYERS
    # --------------------------------------------------------------------------
    # 1. JWT Authentication: Validates the incoming Bearer Token.
    authentication_classes = [JWTAuthentication]
    
    # 2. Permissions: Restricts access to authenticated users only.
    permission_classes = [permissions.IsAuthenticated]

    # SERVER-FIRST INTEGRITY RULE
    # --------------------------------------------------------------------------
    def perform_create(self, serializer):
        """
        Ensures data is validated and processed by the Django server 
        before committing to the database and responding to the client.
        """
        # Save the instance to the database
        serializer.save()