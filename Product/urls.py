from django.urls import path, include, re_path

from .views import ALLCategoryView, GetAllLowlevelTopicView, GetAllMidlevelTopicView, GetMidlevelTopic,ShopLandingView,CreateMidlevelTopicView,CreateProductTopicView,CreateToplevelTopicView,GetAllToplevelTopicView,GetAllProductTopicView,CreateLowLevelTopicView,CreateFieldTopicView,GetMidlevelTopic, SingleLowlevelTopic, SingleMidlevelTopic, SingleProductTopic, SingleToplevelTopic,DeleteLowlevelTopicView,DeleteMidlevelTopicView,DeleteProductTopicView,DeleteToplevelTopicView
app_name = 'Product'
urlpatterns = [

    path("all_categories", ALLCategoryView.as_view(), name="all_categories"),
    path("shop_landing", ShopLandingView.as_view(), name="shop_landing"),
    path("midlevel_topic", CreateMidlevelTopicView.as_view(), name="create_midlevel_topic"),
    path("toplevel_topic", CreateToplevelTopicView.as_view(), name="create_toplevel_topic"),
    path("lowlevel_topic", CreateLowLevelTopicView.as_view(), name="create_lowlevel_topic"),
    path("product_topic", CreateProductTopicView.as_view(), name="create_product_topic"),
    path("delete_midlevel_topic", DeleteMidlevelTopicView.as_view(), name="delete_midlevel_topic"),##api_code:delete 108
    path("delete_toplevel_topic", DeleteToplevelTopicView.as_view(), name="delete_toplevel_topic"),##api_code:delete 109
    path("delete_lowlevel_topic", DeleteLowlevelTopicView.as_view(), name="delete_lowlevel_topic"),##api_code:delete 110
    path("delete_product_topic", DeleteProductTopicView.as_view(), name="delete_product_topic"),##api_code:delete 111
    # path("get_all_midlevel_topic", GetAllMidlevelTopicView.as_view(), name="all_get_midlevel_topic"),
    path("get_all_toplevel_topic", GetAllToplevelTopicView.as_view(), name="get_all_toplevel_topic"),##api_code 101
    path("get_all_lowlevel_topic", GetAllLowlevelTopicView.as_view(), name="get_lowlevel_topic"),##api_code 102
    path("get_all_product_topic", GetAllProductTopicView.as_view(), name="get_all_product_topic"),##api_code 103
    path("create_field_topic", CreateFieldTopicView.as_view(), name="create_field_topic"),
    path("get_all_midlevel_topic", GetMidlevelTopic.as_view(), name="get_midelevel_topic"),##api_coed:100
    path("single_toplevel_topic", SingleToplevelTopic.as_view(), name="single_toplevel_topic"),##api_coed:get"104
    path("single_midlevel_topic", SingleMidlevelTopic.as_view(), name="single_midlevel_topic"),##api_coed:get"105
    path("single_lowlevel_topic", SingleLowlevelTopic.as_view(), name="single_lowlevel_topic"),##api_coed:get"106
    path("single_product_topic", SingleProductTopic.as_view(), name="single_product_topic"),##api_coed:get"107

]