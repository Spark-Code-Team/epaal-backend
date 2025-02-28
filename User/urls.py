from django.urls import path, include, re_path
from User.views import (
    AddProductToCardView,
    ConfirmAddressView,
    HomeView,
    LoginView,
    MyCartView,
    ReplaceCartCardView,
    SendOTP,
    LogoutView,
    ConfirmInformationView,
    SendSecondPhoneOTP,
    ShowAddressView,
    ProfileView,UserWalletView,
    MyFacilityView,
    MyInstallmentView,
    BuyProductView,
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
    path('profile/', ProfileView.as_view(), name='profile'),
    path('wallet/', UserWalletView.as_view(), name='wallet'),
    path('my_facility/', MyFacilityView.as_view(), name='my_facility'),
    path('my_installment/', MyInstallmentView.as_view(), name='my_installment'),
    path('my_cart/', MyCartView.as_view(), name='my_cart'),
    path('add_product_to_card/', AddProductToCardView.as_view(), name='add_product_to_card'),
    path('replace_cart/', ReplaceCartCardView.as_view(), name='replace_cart'),
    path('buy_products/', BuyProductView.as_view(), name='buy_products'),
    path('send_otp_second_phone_number/', SendSecondPhoneOTP.as_view(), name='send_otp_second_phone_number'),

]