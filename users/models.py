"""
Module: users.models
Description: Re-engineered User model for aXeraf Technologies.
             Supports multi-role RBAC (Admin, Manager, Chef, Waiter).
Architect: Kelvin Chacha
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Extends AbstractUser to support phone-based identity and 4-tier roles.
    Integrates with the 5-Layer Communication Chain.
    """

    # --- Role Constants (The 4-Role Model) ---
    ADMIN = 'ADMIN'
    MANAGER = 'MANAGER'
    CHEF = 'CHEF'
    WAITER = 'WAITER'
    
    ROLE_CHOICES = (
        (ADMIN, 'Admin/System Owner'),
        (MANAGER, 'Business Manager'),
        (CHEF, 'Kitchen Controller'),
        (WAITER, 'Service Waiter'),
    )
    
    # --- Custom Fields ---
    
    phone_number = models.CharField(
        max_length=15, 
        unique=True,
        help_text="Primary identifier for system login."
    )
    
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default=WAITER,
        db_index=True # Added index for faster filtering in large datasets
    )
    
    is_default_password = models.BooleanField(
        default=True,
        help_text="Security flag to force password reset on first login."
    )

    # --- Authentication Configuration ---
    
    # Critical: Uses phone_number for authentication logic
    USERNAME_FIELD = 'phone_number'
    
    # Required for 'python manage.py createsuperuser'
    REQUIRED_FIELDS = ['username'] 

    class Meta:
        verbose_name = "System User"
        verbose_name_plural = "System Users"

    def __str__(self):
        return f"{self.phone_number} - {self.get_role_display()}"