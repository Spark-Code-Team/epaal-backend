from django.urls import path, include, re_path

from .views import ConnectMidlevelToProviderBranchView, ShopView,ALLShopView,SingleShopView,GetBoundBranchOneMidTopicView,UnboundBranchOneMidTopicView,GetAllWaitingFacilityView
app_name = 'Admin'
urlpatterns = [

    path("create_shop", ShopView.as_view(), name="create_shop"),
    path("get_all_shops", ALLShopView.as_view(), name="get_all_shop_veiw"),
    path("shop", SingleShopView.as_view(), name="get_shop_veiw"),
    path("get_all_waiting_facility", GetAllWaitingFacilityView.as_view(), name="get_shop_veiw"),
    # path("bound_provider_branch_single_midtopic", GetBoundBranchOneMidTopicView.as_view(), name="get_bound_provider_branch_single_midtopic"),
    # path("unbound_provider_branch_single_midtopic", UnboundBranchOneMidTopicView.as_view(), name="get_unbound_provider_branch_single_midtopic"),
    # path("connect_midlevel_to_provider_branch", ConnectMidlevelToProviderBranchView.as_view(), name="connect_midlevel_to_provider_branch"),

]