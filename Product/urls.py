from django.urls import path, include, re_path

from .views import ALLCategory
app_name = 'Product'
urlpatterns = [

    path("all_categories", ALLCategory.as_view(), name="all_categories"),

]