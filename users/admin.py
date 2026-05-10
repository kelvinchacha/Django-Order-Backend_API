"""
Module: users.admin
Description: High-level Admin panel configuration for Identity and Access Management (IAM).
             Customized for Phone Number authentication and RBAC monitoring.
Architect: Kelvin Chacha
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    """
    Architectural customization of the Django Admin interface 
    to handle Kelvin's custom User model and role-based permissions.
    """
    model = User
    
    # Visual Matrix: What the Manager sees in the staff list view
    list_display = ('phone_number', 'username', 'role', 'is_active', 'is_default_password')
    
    # Audit Filters: Quickly isolate Staff by their operational roles
    list_filter = ('role', 'is_staff', 'is_active')
    
    # Search Optimization: Indexed fields for rapid staff retrieval
    search_fields = ('phone_number', 'username')
    ordering = ('phone_number',)

    # Form Configuration: Integrating Business Logic into User Management
    # Adding our custom fields to the standard User change form
    fieldsets = UserAdmin.fieldsets + (
        ('aXeraf Business Logic', {'fields': ('role', 'phone_number', 'is_default_password')}),
    )
    
    # Adding our custom fields to the User creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('aXeraf Business Logic', {
            'fields': ('role', 'phone_number', 'is_default_password'),
        }),
    )

# Official Registration of the IAM Model
admin.site.register(User, CustomUserAdmin)