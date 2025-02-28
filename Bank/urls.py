from django.urls import path, include, re_path
from .views import (GetAllFacilityView,CreateFacilityView,ConfirmGradeView,SubmitDigitalView,SubmitPhysicalView,DigitalSignitureView,SendCodeGetawayView,
                    PrePaymentView,InquiryUserFacilityView,GetUserFacilityView, UserCretionStatusView)
app_name = 'Bank'
urlpatterns = [

    path("get_all_facility", GetAllFacilityView.as_view(), name="get_top_level_topic"),
    path("create_facility", CreateFacilityView.as_view(), name="create_facility"),#level 1 2
    path("confirm_grade", ConfirmGradeView.as_view(), name="confirm_grade"),#level 3
    path("submit_digital", SubmitDigitalView.as_view(), name="submit_digital"),#level 4 submit
    path("submit_physical", SubmitPhysicalView.as_view(), name="submit_physical"),#level 5 submit
    path("digital_signiture", DigitalSignitureView.as_view(), name="digital_signiture"),#level 6
    path("send_code_getaway_prepayment", SendCodeGetawayView.as_view(), name="send_code_getaway_prepayment"),#level 7
    path("prepayment", PrePaymentView.as_view(), name="prepayment"),#level 7
    path("inquiry_user_facility", InquiryUserFacilityView.as_view(), name="inquiry_user_facility"),
    path("user_craete_status", UserCretionStatusView.as_view(), name="user_craete_status"),
    # path("get_user_facility", GetUserFacilityView.as_view(), name="get_user_facility"),

    
]