from django.shortcuts import render
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db import IntegrityError, transaction
import datetime
from Bank.serializers import FacilityUseerSerialiser, GetUserDocumentSerializer
from Shop.models import ShopRequest
from Shop.serializers import ShopRequestSerializer
from User.models import CreditWallet, UserCreditTransaction
from .models import Shop,Provider,ProviderBranch
from Product.models import MidlevelTopic,MidlevelTopicProviderBranch
from User.serializers import UserRegisterSerializer
from .serializers import ProviderBranchSerializer, ProviderBranchWithProviderSerializer, ShopSerializer,AllShopSerializer,SingleShopSerializer,MidlevelTopicProviderBranchSerializer
from django.db.models.signals import pre_save
from Bank.models import UserFacility
from Bank.models import UserDocumetn,UserInstallment
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
        

class GetAllWaitingFacilityView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        if request.user.role.name != "admin":
            return Response({"error":"you are not admin"},status=status.HTTP_400_BAD_REQUEST)
        
        if UserFacility.objects.filter(level__in=["waiting_digital","waiting_physical","final_waiting"],status="in_progress").exists() == False:
            return Response({"data":{}},status=status.HTTP_200_OK)
        user_facilities=UserFacility.objects.filter(level__in=["waiting_digital","waiting_physical","final_waiting"],status="in_progress")
        ser_data=FacilityUseerSerialiser(instance=user_facilities,many=True)
        return Response({"data":ser_data.data},status=status.HTTP_200_OK)

class ConfirmWaitingDigitalView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self,request):
        if request.user.role.name != "admin":
            return Response({"error":"you are not admin"},status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("user_facility_id") is None or request.data["user_facility_id"] is None:
            return Response({"error":"send user_facility_id"},status=status.HTTP_400_BAD_REQUEST)
        if not UserFacility.objects.filter(id=request.data["user_facility_id"]).exists():
            return Response({"error":"user_facility not found"},status=status.HTTP_404_NOT_FOUND)
        user_facility=UserFacility.objects.get(id=request.data["user_facility_id"])
        if (user_facility.status != "in_progress") or (user_facility.level != "waiting_digital") or user_facility.level_number != 4:
            return Response({"error":"user_facility is not in waiting_digital level"},status=status.HTTP_400_BAD_REQUEST)
        
        user_facility.level="submit_physical"
        user_facility.level_number=5
        user_facility.save()
        return Response({"data":"user_facility level changed to submit_physical"},status=status.HTTP_200_OK)
        

class ConfirmWaitingPhysicalView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self,request):
        if request.user.role.name != "admin":
            return Response({"error":"you are not admin"},status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("user_facility_id") is None or request.data["user_facility_id"] is None:
            return Response({"error":"send user_facility_id"},status=status.HTTP_400_BAD_REQUEST)
        if not UserFacility.objects.filter(id=request.data["user_facility_id"]).exists():
            return Response({"error":"user_facility not found"},status=status.HTTP_404_NOT_FOUND)
        user_facility=UserFacility.objects.get(id=request.data["user_facility_id"])
        if (user_facility.status != "in_progress") or (user_facility.level != "waiting_physical") or user_facility.level_number != 5:
            return Response({"error":"user_facility is not in waiting_physical level"},status=status.HTTP_400_BAD_REQUEST)
        user_facility.level="digital_signiture"
        user_facility.level_number=6
        user_facility.save()
        return Response({"data":"user_facility level changed to digital_signiture"},status=status.HTTP_200_OK)


class ConfirmFinalWaitingView(APIView):

    permission_classes = (IsAuthenticated,)

    def canculate_installment(self,num_of_instalmment,year_percent,cost):
        month_percent=year_percent/1200
        numerator=cost*month_percent
        denominator=1-pow(month_percent+1,(-1*num_of_instalmment))
        return numerator/denominator

    def post(self,request):
        if request.user.role.name != "admin":
            return Response({"error":"you are not admin"},status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("user_facility_id") is None or request.data["user_facility_id"] is None:
            return Response({"error":"send user_facility_id"},status=status.HTTP_400_BAD_REQUEST)
        if not UserFacility.objects.filter(id=request.data["user_facility_id"]).exists():
            return Response({"error":"user_facility not found"},status=status.HTTP_404_NOT_FOUND)
        user_facility=UserFacility.objects.get(id=request.data["user_facility_id"])
        if (user_facility.status != "in_progress") or (user_facility.level != "final_waiting") or user_facility.level_number != 8:
            return Response({"error":"user_facility is not in final_waiting level"},status=status.HTTP_400_BAD_REQUEST)

        new_percent=user_facility.choosen_facility_installment_number.number_of_installment/12
        converted_percent=float(user_facility.evaam_subscripton_percent)/100
        evaam_value=int(user_facility.given_value)*converted_percent*new_percent
        charge_price=int(user_facility.given_value)-evaam_value
        charge_price_str=str(int(charge_price))
        user_facility.status="installment"
        user_facility.save()
        if CreditWallet.objects.filter(user=user_facility.user).exists():
            user_wallet=CreditWallet.objects.get(user=user_facility.user)
        else:
            user_wallet=CreditWallet.objects.create(user=user_facility.user,balance=0.0)

        user_wallet.balance+=charge_price
        user_wallet.save()
        number_of_installment=user_facility.choosen_facility_installment_number.number_of_installment
        UserCreditTransaction.objects.create(credit_wallet=user_wallet,value=charge_price,type="bank_deposite",is_booster=True)
        result=self.canculate_installment(number_of_installment,float(user_facility.bank_interest_percent),float(user_facility.given_value))
        for number in range(1,number_of_installment+1):
            UserInstallment.objects.create(
                user_facility=user_facility,
                installment_number=number,
                amount=result,
                due_date=datetime.datetime.now() + datetime.timedelta(days=30 * number),
                final_amount=result,
                status="not_paid"
            )
        text= f'*ایوام*\n درخواست تسهیلات شما تأیید شد و کیف پول اعتباری  شما مبلغ {charge_price_str} تومان شارژ شد.'
        print(text)
        data = {'from': '50002710054854', 'to':user_facility.user.phone_number, 'text':text}
        response = requests.post('https://console.melipayamak.com/api/send/simple/2d475adf0f3f4fa3bf59f1a99eed0712', json=data)
        return Response({"data":"user_facility status changed to done"},status=status.HTTP_200_OK)
    
class RejectFacilityView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self,request):
        if request.user.role.name != "admin":
            return Response({"error":"you are not admin"},status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("user_facility_id") is None or request.data["user_facility_id"] is None:
            return Response({"error":"send user_facility_id"},status=status.HTTP_400_BAD_REQUEST)
        if not UserFacility.objects.filter(id=request.data["user_facility_id"]).exists():
            return Response({"error":"user_facility not found"},status=status.HTTP_404_NOT_FOUND)
        user_facility=UserFacility.objects.get(id=request.data["user_facility_id"])
        if user_facility.status != "in_progress":
            return Response({"error":"user_facility is not in in_progress status"},status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("reject_text") is None or request.data["reject_text"]=="":
            return Response({"error":"send reject_text"},status=status.HTTP_400_BAD_REQUEST)
        user_facility.reject_reason_text=request.data["reject_text"]
        user_facility.status="cancled"
        user_facility.save()
        return Response({"data":"user_facility status changed to reject"},status=status.HTTP_200_OK)
    
class GetUserFileView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(sself,request):
        if request.user.role.name != "admin":
            return Response({"error":"you are not admin"},status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("user_facility_id") is None or request.data["user_facility_id"] is None:
            return Response({"error":"send user_facility_id"},status=status.HTTP_400_BAD_REQUEST)
        if not UserFacility.objects.filter(id=request.data["user_facility_id"]).exists():
            return Response({"error":"user_facility not found"},status=status.HTTP_404_NOT_FOUND)
        user_facility=UserFacility.objects.get(id=request.data["user_facility_id"])
        if user_facility.status != "in_progress":
            return Response({"error":"user_facility is not in in_progress status"},status=status.HTTP_400_BAD_REQUEST)
        
        if UserDocumetn.objects.filter(user_facility=request.data["user_facility_id"]).exists():
            user_docs=UserDocumetn.objects.filter(user_facility=request.data["user_facility_id"])
            ser_data=GetUserDocumentSerializer(instance=user_docs,many=True,context={"request":request})
            return Response({"data":ser_data.data},status=status.HTTP_200_OK)
        else:
            return Response({"data":[]},status=status.HTTP_200_OK)


class GetSingleShopRequestView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        if request.user.role.name!="admin":
            return Response({"message":"You can not access this url"},status=status.HTTP_403_FORBIDDEN)
        if request.query_params.get("shop_request_id") is None or request.query_params["shop_request_id"] == "":
            return Response({"message":"send shop_request_id"},status=status.HTTP_400_BAD_REQUEST)
        if not ShopRequest.objects.filter(id=request.query_params["shop_request_id"]).exists():
            return Response({"message":"shop_request not found"},status=status.HTTP_404_NOT_FOUND)
        shop_request=ShopRequest.objects.get(id=request.query_params["shop_request_id"])

        serializer = ShopRequestSerializer(shop_request)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetAllShopRequestView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        if request.user.role.name!="admin":
            return Response({"message":"You can not access this url"},status=status.HTTP_403_FORBIDDEN)
        if ShopRequest.objects.filter(is_confirmed=False).exists() == False:
            return Response({"data":{}},status=status.HTTP_200_OK)
        return Response({"data":ShopRequestSerializer(instance=ShopRequest.objects.filter(is_confirmed=False),many=True).data},status=status.HTTP_200_OK) 
