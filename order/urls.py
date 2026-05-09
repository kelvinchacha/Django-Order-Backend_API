from django.urls import path
from .views import OdaList

urlpatterns = [
    path('oda/', OdaList.as_view(), name='oda-list'),
]
