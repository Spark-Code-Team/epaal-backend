from django.urls import path, include, re_path
from User.views import (
    ConfirmAddressView,
    HomeView,
    LoginView,
    SendOTP,
    LogoutView,
    ConfirmInformationView,
    ShowAddressView
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
    path('home/', HomeView.as_view(), name='home'),
    path('confirm_information/', ConfirmInformationView.as_view(), name='confirm_information'),
    path('show_address/', ShowAddressView.as_view(), name='show_address'),
    path('confirm_address/', ConfirmAddressView.as_view(), name='confirm_address'),

]