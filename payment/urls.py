from django.urls import path
from .views import PaymentCreate, DailySummaryView

urlpatterns = [
    path('process/', PaymentCreate.as_view(), name='payment-process'),
    path('summary/', DailySummaryView.as_view(), name='daily-summary'),
]