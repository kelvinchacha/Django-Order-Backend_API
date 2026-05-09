"""
Main URL Configuration for the Order System.
Developed by: Kelvin Chacha
Architecture: N-Tier with Modular Routing
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Django Administration Panel
    path('admin/', admin.site.urls), 
    
    # --- API Endpoints ---
    
    # 1. Identity & Access Management (Hapa ndipo palipokosekana)
    # Hii itashughulikia Login na Token Refresh kitalamu
    path('api/users/', include('users.urls')), 

    # 2. Business Logic: Order Management System
    path('api/oda/', include('order.urls')),

    # --- API Documentation (Swagger & OpenAPI) ---
    # Inasaidia kuona ramani ya API zako kipro kupitia browser
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]