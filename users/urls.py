from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyTokenObtainPairView

urlpatterns = [
    # Hii itakuwa: http://127.0.0.1:8000/api/users/login/
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Hii itakuwa: http://127.0.0.1:8000/api/users/token/refresh/
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
