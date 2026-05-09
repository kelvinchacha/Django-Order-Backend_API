"""
Module: users.views
Description: Identity and Access Management (IAM) logic. 
             Handles custom JWT token generation with role-based payloads.
Developed by: Kelvin Chacha
"""

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Customizing the JWT payload to include user-specific metadata.
    This enables the React Native frontend to handle conditional routing 
    based on the user's role and security status.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Custom claims for the Communication Chain (Layer 3: Context)
        token['username'] = user.username
        token['role'] = user.role
        token['is_default_password'] = user.is_default_password
        
        return token

    def validate(self, attrs):
        """
        Enhancing the validation response to include user details 
        directly in the login response body.
        """
        data = super().validate(attrs)
        
        # Hizi data zitarudi kwenye 'response.data' wakati wa login
        data['user'] = {
            'username': self.user.username,
            'phone_number': self.user.phone_number,
            'role': self.user.role,
            'is_default_password': self.user.is_default_password
        }
        
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    """
    The main login endpoint (Security Layer).
    Accepts phone_number and password to return JWT access/refresh tokens.
    """
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny] # Inaruhusu kila mtumiaji kujaribu kuingia