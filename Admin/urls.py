from django.urls import path, include, re_path

from .views import ShopView,ALLShopView,SingleShopView,GetBranchOneMidTopicView
app_name = 'Admin'
urlpatterns = [

    path("create_shop", ShopView.as_view(), name="create_shop"),
    path("get_all_shops", ALLShopView.as_view(), name="get_all_shop_veiw"),
    path("shop", SingleShopView.as_view(), name="get_shop_veiw"),
    path("get_provider_branch_single_midtopic", GetBranchOneMidTopicView.as_view(), name="get_provider_branch_single_midtopic"),

]