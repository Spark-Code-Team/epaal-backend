from django.shortcuts import render
from rest_framework.views import APIView
from User.models import JibitToken
from .models import Facility
from .serializers import FacilitySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from persian_tools.bank import sheba
import datetime
from django.utils import timezone
import requests
# Create your views here.

class GetAllFacilityView(APIView):
    serializer_class = FacilitySerializer
    def get(self, request):
        facilities = Facility.objects.all()
        serializer = FacilitySerializer(facilities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
 
class CreateFacilityView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,requset):
        print(requset.data)
        if requset.data.get("sheba_number") is None or requset.data["sheba_number"]=="":
            return Response({"message":" sheba_number is required"},status=status.HTTP_400_BAD_REQUEST)
        if requset.data.get("facility_id") is None or requset.data["facility_id"]=="":
            return Response({"message":" facility_id is required"},status=status.HTTP_400_BAD_REQUEST)
        if not Facility.objects.filter(id=requset.data["facility_id"]).exists():
            return Response({"message":" facility_id is not valid"},status=status.HTTP_400_BAD_REQUEST)
        facility=Facility.objects.get(id=requset.data["facility_id"])

        if sheba.validate(requset.data["sheba_number"])==False:
            return Response({"message":" sheba_number is not valid"},status=status.HTTP_400_BAD_REQUEST)
        if sheba.bank_data(requset.data["sheba_number"])["nickname"]!=facility.bank.name:
            return Response({"message":" sheba_number is not valid"},status=status.HTTP_400_BAD_REQUEST)
        
        if JibitToken.objects.filter(created_at__gte=timezone.now()-datetime.timedelta(days=1)).exists():
            jibit_token=JibitToken.objects.get(created_at__gte=timezone.now()-datetime.timedelta(days=24))
            access_token=jibit_token.access_token
        else:
            response = requests.post('https://napi.jibit.ir/ide/v1/tokens/generate', json={"apiKey":"cvYDi4nzvP","secretKey":"5Ioyhh9MDbjA19_JQi16CJWI9"})
            JibitToken.objects.create(access_token=response.json()["accessToken"],refresh_token=response.json()["refreshToken"])
            access_token=response.json()["accessToken"]
        header={"Authorization":f"Bearer {access_token}"}
        path=f"https://napi.jibit.ir/ide//v1/ibans?value={requset.data['sheba_number']}"
        response = requests.get(path,headers=header)

        if response.status_code<200 or response.status_code>=300:
            return Response({"message":" sheba_number is not valid"},status=status.HTTP_400_BAD_REQUEST)
        
        print(sheba.validate(requset.data["sheba_number"]))
        print(sheba.bank_data(requset.data["sheba_number"]))
        return Response({"data":"of"},status=status.HTTP_200_OK) 