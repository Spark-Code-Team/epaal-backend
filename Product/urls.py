from django.urls import path, include, re_path

from .views import ALLCategoryView,ShopLandingView
app_name = 'Product'
urlpatterns = [

    path("all_categories", ALLCategoryView.as_view(), name="all_categories"),
    path("shop_landing", ShopLandingView.as_view(), name="shop_landing"),

]