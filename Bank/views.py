import random
import string
from django.shortcuts import render
from rest_framework.views import APIView
from User.models import JibitToken
from .models import Facility
from .serializers import FacilityDocumentSerializer, FacilitySerializer, FacilityUseerSerialiser, UserDocumentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from persian_tools.bank import sheba
import datetime
from django.utils import timezone
import requests
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UserFacility,FacilityInstallmentNumber,SubGrade,FacilityDocument,UserDocumetn
# Create your views here.

class GetAllFacilityView(APIView):
    serializer_class = FacilitySerializer
    def get(self, request):
        facilities = Facility.objects.all()
        serializer = FacilitySerializer(facilities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
 
class CreateFacilityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        if UserFacility.objects.filter(user=request.user,status__in=["in_progress","installment"]).exists():
            return Response({"message":"You have a facility in progress or installment"},status=status.HTTP_400_BAD_REQUEST)
        
        if (request.user.confirmed_data is False) or (request.user.confirmed_address is False):
            return Response({"message":"please complete information and address first"},status=status.HTTP_403_FORBIDDEN)
        
        if request.data.get("sheba_number") is None or request.data["sheba_number"]=="":
            return Response({"message":"sheba_number is required"},status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get("facility_id") is None or request.data["facility_id"]=="":
            return Response({"message":"facility_id is required"},status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get("choosen_value") is None or request.data["choosen_value"]=="":
            return Response({"message":"choosen_value is required"},status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get("facility_installment_id") is None or request.data["facility_installment_id"]=="":   
            return Response({"message":"facility_installment_id is required"},status=status.HTTP_400_BAD_REQUEST)
        
        if not Facility.objects.filter(id=request.data["facility_id"]).exists():
            return Response({"message":"facility_id is not found"},status=status.HTTP_400_BAD_REQUEST)
        
        facility=Facility.objects.get(id=request.data["facility_id"])

        if sheba.validate(request.data["sheba_number"])==False:
            return Response({"message":" sheba_number is not valid"},status=status.HTTP_400_BAD_REQUEST)
        
        if sheba.bank_data(request.data["sheba_number"])["nickname"]!=facility.bank.nickname:
            return Response({"message":" sheba bank name is not valid"},status=status.HTTP_400_BAD_REQUEST)
        
        if int(facility.max_value)<int(request.data["choosen_value"]):
            return Response({"message":" choosen_value is too much"},status=status.HTTP_400_BAD_REQUEST)
        
        if JibitToken.objects.filter(created_at__gte=timezone.now()-datetime.timedelta(days=1)).exists():
            jibit_token=JibitToken.objects.get(created_at__gte=timezone.now()-datetime.timedelta(days=1))
            access_token=jibit_token.access_token
        else:
            response = requests.post('https://napi.jibit.ir/ide/v1/tokens/generate', json={"apiKey":"cvYDi4nzvP","secretKey":"5Ioyhh9MDbjA19_JQi16CJWI9"})
            JibitToken.objects.create(access_token=response.json()["accessToken"],refresh_token=response.json()["refreshToken"])
            access_token=response.json()["accessToken"]
        header={"Authorization":f"Bearer {access_token}"}
        path=f"https://napi.jibit.ir/ide//v1/ibans?value={request.data['sheba_number']}"
        response = requests.get(path,headers=header)
        if response.status_code<200 or response.status_code>=300:
            return Response({"message":" sheba number is not valid"},status=status.HTTP_400_BAD_REQUEST)
        
        if response.json()["ibanInfo"]["bank"]!=facility.bank.jiibit_bank_naem:
            return Response({"message":"name of bank is not ok"},status=status.HTTP_400_BAD_REQUEST)
        
        if response.json()["ibanInfo"]["status"]!="ACTIVE":
            return Response({"message":" sheba_number is not active"},status=status.HTTP_400_BAD_REQUEST)
        
        if len(response.json()["ibanInfo"]["owners"])>1:
            return Response({"message":" account is not valid"},status=status.HTTP_400_BAD_REQUEST)
        
        if FacilityInstallmentNumber.objects.filter(facility=facility,id=int(request.data["facility_installment_id"])).exists()==False:
            return Response({"message":" facility_installment_id is not valid"},status=status.HTTP_400_BAD_REQUEST)
            
        user_facility=UserFacility.objects.create(
                                    user=request.user,
                                    facility=facility,
                                    status="in_progress",
                                    max_value=facility.max_value,
                                    evaam_subscripton_percent=facility.evaam_subscripton_percent,
                                    pre_payment_percent=facility.pre_payment_percent,
                                    bank_interest_percent=facility.bank_interest_percent,
                                    level="grade",level_number=3,
                                    choosen_value=request.data["choosen_value"],
                                    sub_grade=None,
                                    choosen_facility_installment_number=FacilityInstallmentNumber.objects.get(id=int(request.data["facility_installment_id"])),
                                    sheba_number=request.data["sheba_number"]
                                    )
        
        return Response({"data":"facility created successfuly"},status=status.HTTP_200_OK) 
    
class ConfirmGradeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        if UserFacility.objects.filter(user=request.user,level="grade",level_number=3,status="in_progress").exists()==False:
            return Response({"message":"You do not have any facility in progress"},status=status.HTTP_400_BAD_REQUEST)
        user_facility=UserFacility.objects.get(user=request.user,level="grade",level_number=3,status="in_progress") 
        sub_grade_array=["A3","A2","A1","B3","B2","B1"]
        sub_grade_name=random.choice(sub_grade_array)
        sub_grade=SubGrade.objects.get(name=sub_grade_name)
        grade_name=sub_grade.grade.name 
        if grade_name not in ["A","B"]:
            return Response({"message":"your grade is ot enough"},status=status.HTTP_400_BAD_REQUEST)
        
        user_facility.given_value=user_facility.choosen_value
        user_facility.sub_grade_id=sub_grade
        user_facility.level="submit_digital"
        user_facility.level_number=4
        user_facility.save()
        return Response({"message":"level 3 is done"},status=status.HTTP_200_OK)
    

class SubmitDigitalView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes=(MultiPartParser,FormParser)

    def get(self,request):
        if UserFacility.objects.filter(user=request.user,level__in=["submit_digital","waiting_digital"],level_number=4,status="in_progress").exists()==False:
            return Response({"message":"You do not have any facility in this level"},status=status.HTTP_400_BAD_REQUEST)
        if UserFacility.objects.filter(user=request.user,level="submit_digital",level_number=4,status="in_progress").exists():
            user_facility=UserFacility.objects.get(user=request.user,level="submit_digital",level_number=4,status="in_progress") 
            facility_docs=FacilityDocument.objects.filter(facility=user_facility.facility)
            ser_data=FacilityDocumentSerializer(instance=facility_docs,many=True)
            return Response({"data":ser_data.data,"status":"submit_digital"},status=status.HTTP_200_OK)
        elif UserFacility.objects.filter(user=request.user,level="waiting_digital",level_number=4,status="in_progress").exists():
            return Response({"data":None,"status":"waiting_digital"},status=status.HTTP_200_OK)
    
    def post(self,request):
        if UserFacility.objects.filter(user=request.user,level="submit_digital",level_number=4,status="in_progress").exists()==False:
            return Response({"message":"You do not have any facility in progress"},status=status.HTTP_400_BAD_REQUEST)
        user_facility=UserFacility.objects.get(user=request.user,level="submit_digital",level_number=4,status="in_progress") 

        grouped_data = []

        index = 0
        while f"data[{index}][id]" in request.data:
            file_obj = request.data.get(f"data[{index}][file]")
            value_obj = request.data.get(f"data[{index}][value]")
            id_obj = request.data.get(f"data[{index}][id]")

            grouped_data.append({
                "file": file_obj if file_obj else None,
                "value": value_obj if value_obj else None,
                "document": FacilityDocument.objects.get(id=id_obj).id,
                "user_facility": user_facility.id,
                "status":"not_confirmed"
            })
            index += 1
        print(grouped_data)

        ser_data=UserDocumentSerializer(data=grouped_data, many=True)
        if ser_data.is_valid(raise_exception=True):
            ser_data.save()
        user_facility.level="waiting_digital"
        user_facility.level_number=4
        user_facility.save()
        return Response({"message":"level 4 is done"},status=status.HTTP_200_OK)
    
class SubmitPhysicalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        if UserFacility.objects.filter(user=request.user,level__in=["submit_physical","waiting_physical"],level_number=5,status="in_progress").exists()==False:
            return Response({"message":"You do not have any facility in this level"},status=status.HTTP_400_BAD_REQUEST)
        if UserFacility.objects.filter(user=request.user,level="submit_physical",level_number=5,status="in_progress").exists():
            return Response({"status":"submit_physical"},status=status.HTTP_200_OK)
        elif UserFacility.objects.filter(user=request.user,level="waiting_physical",level_number=5,status="in_progress").exists():
            return Response({"status":"waiting_physical"},status=status.HTTP_200_OK)

    def post(self,request):
        if UserFacility.objects.filter(user=request.user,level="submit_physical",level_number=5,status="in_progress").exists()==False:
            return Response({"message":"You do not have any facility in progress"},status=status.HTTP_400_BAD_REQUEST)
        user_facility=UserFacility.objects.get(user=request.user,level="submit_physical",level_number=5,status="in_progress")
        user_facility.level="waiting_physical"
        user_facility.save()
        return Response({"message":"now you are pendinf for admin confirmation"},status=status.HTTP_200_OK)
    

class DigitalSignitureView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        if UserFacility.objects.filter(user=request.user,level="digital_signiture",level_number=6,status="in_progress").exists()==False:
            return Response({"message":"You do not have any facility in this level"},status=status.HTTP_400_BAD_REQUEST)
        user_facility=UserFacility.objects.get(user=request.user,level="digital_signiture",level_number=6,status="in_progress")
        user_facility.level_number=7
        user_facility.level="prepayment"
        user_facility.save()
        return Response({"message":"level 6 is done"},status=status.HTTP_200_OK)

class SendCodeGetawayView(APIView):
    permission_classes = [IsAuthenticated]

    def generate_otp(self):
        return ''.join(random.choices(string.digits, k=8))
    
    def post(self,request):
        if UserFacility.objects.filter(user=request.user,level="prepayment",level_number=7,status="in_progress").exists()==False:
            return Response({"message":"You do not have any facility in this level"},status=status.HTTP_400_BAD_REQUEST)
        user_facility=UserFacility.objects.get(user=request.user,level="prepayment",level_number=7,status="in_progress")
        string_pre_payment=str(int(float(user_facility.given_value)*(float(user_facility.pre_payment_percent)/100)))
        data = {'from': '50002710054854', 'to': request.user.phone_number, 'text': f'*ایوام*\nخرید از ایوام\nمبلغ:{string_pre_payment} تومان\nکد: {self.generate_otp()}\n'}
        response = requests.post('https://console.melipayamak.com/api/send/simple/2d475adf0f3f4fa3bf59f1a99eed0712', json=data)
        if response.json()["status"]=="ارسال موفق بود":
            return Response({"message":"با موفقیت ارسال شد"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"ارسال کد با خطایی مواجه شد."},status=status.HTTP_400_BAD_REQUEST)
        
class PrePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        if UserFacility.objects.filter(user=request.user,level="prepayment",level_number=7,status="in_progress").exists()==False:
            return Response({"message":"You do not have any facility in this level"},status=status.HTTP_400_BAD_REQUEST)
        user_facility=UserFacility.objects.get(user=request.user,level="prepayment",level_number=7,status="in_progress")
        string_pre_payment=str(int(float(user_facility.given_value)*(float(user_facility.pre_payment_percent)/100)))
        return Response({"data":string_pre_payment},status=status.HTTP_200_OK)


    def post(self,request):
        if UserFacility.objects.filter(user=request.user,level="prepayment",level_number=7,status="in_progress").exists()==False:
            return Response({"message":"You do not have any facility in this level"},status=status.HTTP_400_BAD_REQUEST)
        user_facility=UserFacility.objects.get(user=request.user,level="prepayment",level_number=7,status="in_progress")
        user_facility.level="final_waiting"
        user_facility.level_number=8
        user_facility.save()
        return Response({"message":"level 7 is done"},status=status.HTTP_200_OK)
    
class InquiryUserFacilityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        if UserFacility.objects.filter(user=request.user,status="in_progress").exists()==False:
            return Response({"data":None},status=status.HTTP_200_OK)
        user_facilities=UserFacility.objects.get(user=request.user,status="in_progress")
        ser_data=FacilityUseerSerialiser(instance=user_facilities)
        return Response({"data":ser_data.data},status=status.HTTP_200_OK)
    
class UserCretionStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        if UserFacility.objects.filter(user=request.user,status__in=["in_progress","installment"]).exists():
            return Response({"data":False,"message":"user can not create new facility"},status=status.HTTP_200_OK)
        else:
            return Response({"data":True,"message":"user can create new facility"},status=status.HTTP_200_OK)
    

    



class GetUserFacilityView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):
        pass