from django.urls import path, include, re_path

from .views import  GetFieldsForCreateProductView, GetToplevelTopicView,GetLowlevelTopicView,GetMidlevelTopicView,GetProductTopicView
app_name = 'Shop'
urlpatterns = [

    path("get_top_level_topic", GetToplevelTopicView.as_view(), name="get_top_level_topic"),
    path("get_mid_level_topic", GetMidlevelTopicView.as_view(), name="get_mid_level_topic"),
    path("get_low_level_topic", GetLowlevelTopicView.as_view(), name="get_low_level_topic"),
    path("get_product_topic", GetProductTopicView.as_view(), name="get_product_topic"),
    path("get_field_for_create_product", GetFieldsForCreateProductView.as_view(), name="get_field_for_create_product"),
    
]