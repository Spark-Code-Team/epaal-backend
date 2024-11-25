from django.urls import path, include, re_path
from User.views import (
    LoginView,
    SendOTP,
    LogoutView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'Users'
urlpatterns = [

    path("send-otp/", SendOTP.as_view(), name="register"),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]