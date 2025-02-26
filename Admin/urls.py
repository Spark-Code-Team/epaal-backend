from django.urls import path, include, re_path

from .views import (ConnectMidlevelToProviderBranchView,
                    ShopView,ALLShopView,SingleShopView,
                    GetBoundBranchOneMidTopicView,
                    UnboundBranchOneMidTopicView,
                    GetAllWaitingFacilityView,
                    ConfirmWaitingDigitalView,
                    ConfirmWaitingPhysicalView,
                    ConfirmFinalWaitingView,
                    RejectFacilityView,
                    GetUserFileView
                    )
app_name = 'Admin'
urlpatterns = [

    path("create_shop", ShopView.as_view(), name="create_shop"),
    path("get_all_shops", ALLShopView.as_view(), name="get_all_shop_veiw"),
    path("shop", SingleShopView.as_view(), name="get_shop_veiw"),
    path("get_all_waiting_facility", GetAllWaitingFacilityView.as_view(), name="get_shop_veiw"),
    path("confirm_waitnig_digital", ConfirmWaitingDigitalView.as_view(), name="confirm_waitnig_digital"),
    path("confirm_waitnig_physical", ConfirmWaitingPhysicalView.as_view(), name="confirm_waitnig_physical"),
    path("confirm_final_waiting", ConfirmFinalWaitingView.as_view(), name="confirm_final_waiting"),
    path("reject_facility", RejectFacilityView.as_view(), name="reject_facility"),
    path("get_user_file", GetUserFileView.as_view(), name="get_user_file"),



    # path("bound_provider_branch_single_midtopic", GetBoundBranchOneMidTopicView.as_view(), name="get_bound_provider_branch_single_midtopic"),
    # path("unbound_provider_branch_single_midtopic", UnboundBranchOneMidTopicView.as_view(), name="get_unbound_provider_branch_single_midtopic"),
    # path("connect_midlevel_to_provider_branch", ConnectMidlevelToProviderBranchView.as_view(), name="connect_midlevel_to_provider_branch"),

]