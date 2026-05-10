"""
Module: payment.urls
Description: Financial endpoint routing for revenue collection.
Architect: Kelvin Chacha
"""

from django.urls import path
from .views import PaymentCreateView, RevenueDashboardView

urlpatterns = [
    # Endpoint ya kusajili malipo mapya kupitia App
    path('process/', PaymentCreateView.as_view(), name='payment-process'),
    
    # Endpoint ya ripoti ya mapato ya siku kwa ajili ya Manager
    path('summary/', RevenueDashboardView.as_view(), name='daily-summary'),
]