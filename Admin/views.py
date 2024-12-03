from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db import IntegrityError, transaction
from User.serializers import UserRegisterSerializer
from .serializers import ShopSerializer
from django.db.models.signals import pre_save
# Create your views here.
class ShopView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        if (request.user.role.name != "admin") or (request.user.is_admin is not True):
            return Response({"error":"you are not admin"},status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                user_ser=UserRegisterSerializer(data=request.data)
                request.data["role"]={"name":"admin_shop"}
                if user_ser.is_valid():
                    shop_admin=user_ser.save()
                    request.data["shop_admin"]=shop_admin.id
                    shop_ser=ShopSerializer(data=request.data)
                    if shop_ser.is_valid():
                        shop=shop_ser.save()
                        created_shop=ShopSerializer(instance=shop)
                        return Response(created_shop.data,status=status.HTTP_200_OK)
                    else:
                        raise ValueError("Shop data is invalid: " + str(shop_ser.errors))
                else:
                    raise ValueError("User data is invalid: " + str(user_ser.errors))
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
