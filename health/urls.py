from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterUserView, LoginView, HealthReportView, api_home
from .views import login_page, register_page, health_page

urlpatterns = [
    path('', api_home, name='api_home'),  
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('health-reports/', HealthReportView.as_view(), name='health_reports'),
    

    # 🔹 Frontend pages
    path('login-page/', login_page, name='login_page'),
    path('register-page/', register_page, name='register_page'),
    path('health/', health_page, name='health'),
]
