from django.urls import path, include, re_path
from User.views import (
    UserRegistration,
    LogoutView,
    CustomTokenObtainPairView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'Users'
urlpatterns = [

    path("register/", UserRegistration.as_view(), name="register"),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]