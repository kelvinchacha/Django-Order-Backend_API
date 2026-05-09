from django.db import models

# Create your models here.
"""
Module: users.models
Description: Custom user model to handle phone-based authentication and 
             role-based access control (RBAC) for the Order System.
Architect: Kelvin Chacha
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Extends the base AbstractUser to support phone_number as the primary identifier.
    Includes business-specific roles and security enforcement flags.
    """

    # --- Role Definitions ---
    # We define roles as constants to avoid hardcoding strings in the logic
    ADMIN = 'ADMIN'
    WAITER = 'WAITER'
    
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (WAITER, 'Waiter'),
    )
    
    # --- Custom Fields ---
    
    # Primary identity field for the business (Unique for each staff)
    phone_number = models.CharField(
        max_length=15, 
        unique=True,
        help_text="Primary identifier for system login."
    )
    
    # Determines the access level within the application
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default=WAITER
    )
    
    # Security Enforcement: True if user must reset their generated password
    is_default_password = models.BooleanField(
        default=True,
        help_text="Forces a password change request on first login."
    )

    # --- Authentication Configuration ---
    
    # Set phone_number as the field used for authentication instead of username
    USERNAME_FIELD = 'phone_number'
    
    # Required when creating a superuser via 'createsuperuser' CLI
    REQUIRED_FIELDS = ['username'] 

    def __str__(self):
        """Returns the string representation of the user."""
        return f"{self.phone_number} ({self.role})"