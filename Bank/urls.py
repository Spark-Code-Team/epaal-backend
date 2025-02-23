from django.urls import path, include, re_path
from .views import GetAllFacilityView
app_name = 'Bank'
urlpatterns = [

    path("get_all_facility", GetAllFacilityView.as_view(), name="get_top_level_topic"),
    
]