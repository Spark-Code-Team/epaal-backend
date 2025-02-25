from django.urls import path, include, re_path
from .views import GetAllFacilityView,CreateFacilityView,ConfirmGradeView
app_name = 'Bank'
urlpatterns = [

    path("get_all_facility", GetAllFacilityView.as_view(), name="get_top_level_topic"),
    path("create_facility", CreateFacilityView.as_view(), name="create_facility"),
    path("confirm_grade", ConfirmGradeView.as_view(), name="confirm_grade"),
    
]