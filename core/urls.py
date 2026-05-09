"""
Main URL Configuration for the Order System.
Developed by: Kelvin Chacha (aXeraf Technologies)
Architecture: N-Tier with Modular Routing
Framework: Django REST Framework with JWT Authentication
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Django Administration Panel
    # Provides a secure interface for superusers to manage the database.
    path('admin/', admin.site.urls), 
    
    # --- API Endpoints ---
    
    # 1. Identity & Access Management (IAM)
    # Handles user registration, login, and JWT token refresh logic.
    path('api/users/', include('users.urls')), 

    # 2. Business Logic: Order Management System (OMS)
    # Refactored from 'oda/' to 'order/' for global naming standards.
    path('api/order/', include('order.urls')),

    # --- API Documentation (Swagger & OpenAPI) ---
    # Generates a professional API map for frontend integration and testing.
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]