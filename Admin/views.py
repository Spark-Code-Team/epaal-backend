from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db import IntegrityError, transaction
from .models import Shop
from User.serializers import UserRegisterSerializer
from .serializers import ShopSerializer,AllShopSerializer,SingleShopSerializer
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


class ALLShopView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        if (request.user.role.name != "admin") or (request.user.is_admin is not True):
            return Response({"error":"you are not admin"},status=status.HTTP_400_BAD_REQUEST)
        shops=Shop.objects.all() 
        if shops:
            ser_data=AllShopSerializer(instance=shops,many=True)
            return Response({"data":ser_data.data},status=status.HTTP_200_OK)
        else:
            return Response({"error":"there is not any shops"},status=status.HTTP_404_NOT_FOUND)
        

class SingleShopView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        if (request.user.role.name != "admin") or (request.user.is_admin is not True):
            return Response({"error":"you are not admin"},status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("shop_id") is None or request.data["shop_id"] is None:
            return Response({"error":"send shop_id"},status=status.HTTP_400_BAD_REQUEST)
        if Shop.objects.filter(id=request.data["shop_id"]).exists():
            shop=Shop.objects.get(id=request.data["shop_id"]) 
            ser_data=SingleShopSerializer(instance=shop)
            return Response({"data":ser_data.data},status=status.HTTP_200_OK)
        else:
            return Response({"error":"shop not found"},status=status.HTTP_404_NOT_FOUND)

    def put(self,request):
        if (request.user.role.name != "admin") or (request.user.is_admin is not True):
            return Response({"error":"you are not admin"},status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("shop_id") is None or request.data["shop_id"] is None:
            return Response({"error":"send shop_id"},status=status.HTTP_400_BAD_REQUEST)
        if Shop.objects.filter(id=request.data["shop_id"]).exists():
            shop=Shop.objects.get(id=request.data["shop_id"]) 
            edited_shop=ShopSerializer(instance=shop,data=request.data,partial=True)
            if edited_shop.is_valid():
                edited_shop.save()
                return Response({"data":edited_shop.data},status=status.HTTP_200_OK)
            else:
                return Response({"error":edited_shop.errors},status=status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response({"error":"shop not found"},status=status.HTTP_404_NOT_FOUND)