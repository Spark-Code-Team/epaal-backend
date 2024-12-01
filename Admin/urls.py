from django.urls import path, include, re_path

from .views import ShopView
app_name = 'Admin'
urlpatterns = [

    path("create_shop", ShopView.as_view(), name="create_shop"),
]