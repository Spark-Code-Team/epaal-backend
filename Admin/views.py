from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db import IntegrityError, transaction
from .models import Shop,Provider,ProviderBranch
from Product.models import MidlevelTopic,MidlevelTopicProviderBranch
from User.serializers import UserRegisterSerializer
from .serializers import ProviderBranchSerializer, ProviderBranchWithProviderSerializer, ShopSerializer,AllShopSerializer,SingleShopSerializer,MidlevelTopicProviderBranchSerializer
from django.db.models.signals import pre_save
# Create your views here.
class ShopView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        if (request.user.role.name != "admin") or (request.user.is_admin is not True):
            return Response({"error":"you are not admin"},status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                request.data["role"]={"name":"shop_admin"}
                user_ser=UserRegisterSerializer(data=request.data)
                if (request.data.get("referrer_code") is not None) and(request.data["referrer_code"]):
                    referrer_code=request.data["referrer_code"]
                else:
                    referrer_code=None
                if user_ser.is_valid():
                    shop_admin=user_ser.create(validated_data=user_ser.validated_data,role={"name":"shop_admin"},referrer_code=referrer_code)
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
        
class GetBoundBranchOneMidTopicView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        if request.user.role.name != "admin":
            return Response({"error":"you are not admin"},status=status.HTTP_400_BAD_REQUEST)
        if (request.query_params.get("midlevel_topic") is None)or (request.query_params["midlevel_topic"] == ""):
            return Response({"error":"send midlevel_topic"},status=status.HTTP_400_BAD_REQUEST)
        if MidlevelTopic.objects.filter(id=request.query_params["midlevel_topic"]).exists():
            midlevel_topic=MidlevelTopic.objects.get(id=request.query_params["midlevel_topic"])
            if MidlevelTopicProviderBranch.objects.filter(midlevel_topic=midlevel_topic).exists():
                provider_branch_list=[]
                provider_branches=MidlevelTopicProviderBranch.objects.filter(midlevel_topic=midlevel_topic)
                for provider_branch_midlevle in provider_branches:
                   provider_branch_list.append(provider_branch_midlevle.provider_branch) 
                ser_data=ProviderBranchWithProviderSerializer(instance=provider_branch_list,many=True)
                return Response({"data":ser_data.data},status=status.HTTP_200_OK)
            else:
                return Response({"error":"provider branch not found"},status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({"error":"midlevel_topic not found"},status=status.HTTP_404_NOT_FOUND)

class UnboundBranchOneMidTopicView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        if request.user.role.name != "admin":
            return Response({"error":"you are not admin"},status=status.HTTP_400_BAD_REQUEST)
        if (request.query_params.get("midlevel_topic") is None)or (request.query_params["midlevel_topic"] == ""):
            return Response({"error":"send midlevel_topic"},status=status.HTTP_400_BAD_REQUEST)
        if MidlevelTopic.objects.filter(id=request.query_params["midlevel_topic"]).exists():
            midlevel_topic=MidlevelTopic.objects.get(id=request.query_params["midlevel_topic"])
            midlevel_providers=MidlevelTopicProviderBranch.objects.filter(midlevel_topic=midlevel_topic)
            provider_ids=[]
            for midlevel_provider in midlevel_providers:
                provider_ids.append(midlevel_provider.provider_branch.provider.id)
            print(provider_ids)
            providers=ProviderBranch.objects.exclude(provider__id__in=provider_ids)
            if providers:
               ser_data=ProviderBranchWithProviderSerializer(instance=providers,many=True) 
               return Response({"data":ser_data.data},status=status.HTTP_200_OK)
            else:
                return Response({"error":"provider branch not found"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error":"midlevel_topic not found"},status=status.HTTP_404_NOT_FOUND)
        

class ConnectMidlevelToProviderBranchView(APIView):
    permission_classes=(IsAuthenticated,)

    def post(self,request):
        if request.user.role.name != "admin":
            return Response({"error":"you are not admin"},status=status.HTTP_400_BAD_REQUEST)
        if (request.data.get("midlevel_topic") is None)or (request.data["midlevel_topic"] == ""):
            return Response({"error":"send midlevel_topic"},status=status.HTTP_400_BAD_REQUEST)
        if (not request.data.get("provider_branch")) or (not isinstance(request.data["provider_branch"], list)) or (not request.data["provider_branch"]):
            return Response({"error":"send a non-empty list of provider_branch ids"},status=status.HTTP_400_BAD_REQUEST)
        if MidlevelTopic.objects.filter(id=request.data["midlevel_topic"]).exists():
            midlevel_topic=MidlevelTopic.objects.get(id=request.data["midlevel_topic"])
            provider_ids=[]
            for provider_branch in MidlevelTopicProviderBranch.objects.filter(midlevel_topic=midlevel_topic):
                provider_ids.append(provider_branch.provider_branch.provider.id)
            provider_of_input=[]
            for provider_branch_id in request.data["provider_branch"]:
                if ProviderBranch.objects.filter(id=provider_branch_id).exists():
                    provider_branch=ProviderBranch.objects.get(id=provider_branch_id)
                    if provider_branch.provider.id in provider_of_input:
                        return Response({"error":"every mid level topic can just connect to on provider branch from a provider"},status=status.HTTP_400_BAD_REQUEST)
                    provider_of_input.append(provider_branch.provider.id)
                    if provider_branch.provider.id in provider_ids:
                        return Response({"error":"every mid level topic can just connect to on provider branch from a provider"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error":"provider_branch not found"},status=status.HTTP_404_NOT_FOUND)

                if MidlevelTopicProviderBranch.objects.filter(midlevel_topic=midlevel_topic,provider_branch=provider_branch).exists():
                    return Response({"error":"provider_branch is already connected to midlevel_topic"},status=status.HTTP_400_BAD_REQUEST)
                
            for provider_branch_id in request.data["provider_branch"]:
                MidlevelTopicProviderBranch.objects.create(midlevel_topic=midlevel_topic,provider_branch=provider_branch)
            return Response({"data":"midlevel_topic connected to provider_branches successfully"},status=status.HTTP_200_OK)

        else:
            return Response({"error":"midlevel_topic not found"},status=status.HTTP_404_NOT_FOUND)