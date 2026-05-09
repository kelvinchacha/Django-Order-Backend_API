"""
Module: users.admin
Description: Admin panel configuration for User management.
             Customized for Phone Number authentication.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    """
    Architectural customization of the Django Admin interface 
    to handle Kelvin's custom User model.
    """
    model = User
    
    # Inaonyesha safu hizi kwenye orodha ya watumiaji
    list_display = ('phone_number', 'username', 'role', 'is_staff', 'is_default_password')
    
    # Inaweka filters upande wa kulia
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    
    # Sehemu za kuongeza na kurekebisha mtumiaji (Form fields)
    fieldsets = UserAdmin.fieldsets + (
        ('Business Logic Fields', {'fields': ('role', 'phone_number', 'is_default_password')}),
    )
    
    # Sehemu ya kutengeneza mtumiaji mpya
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Business Logic Fields', {'fields': ('role', 'phone_number', 'is_default_password')}),
    )
    
    # Namna ya kutafuta watumiaji
    search_fields = ('phone_number', 'username')
    ordering = ('phone_number',)

# Sajili Model yako na CustomAdmin uliyotengeneza
admin.site.register(User, CustomUserAdmin)