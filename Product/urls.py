from django.urls import path, include, re_path

from .views import ALLCategoryView,ShopLandingView,CreateMidlevelTopicView,CreateProductTopicView,CreateToplevelTopicView,GetMidlevelTopicView,GetToplevelTopicView,GetProductTopicView
app_name = 'Product'
urlpatterns = [

    path("all_categories", ALLCategoryView.as_view(), name="all_categories"),
    path("shop_landing", ShopLandingView.as_view(), name="shop_landing"),
    path("create_midlevel_topic", CreateMidlevelTopicView.as_view(), name="create_midlevel_topic"),
    path("create_toplevel_topic", CreateToplevelTopicView.as_view(), name="create_toplevel_topic"),
    path("create_product_topic", CreateProductTopicView.as_view(), name="create_product_topic"),
    path("get_midlevel_topic", GetMidlevelTopicView.as_view(), name="get_midlevel_topic"),
    path("get_toplevel_topic", GetToplevelTopicView.as_view(), name="get_toplevel_topic"),
    path("get_product_topic", GetProductTopicView.as_view(), name="get_product_topic")
]