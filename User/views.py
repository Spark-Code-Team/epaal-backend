
from User.models import CustomUser
from User.serializers import UserRegisterSerializer
from rest_framework.parsers import FileUploadParser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from EvaamBack import settings
from Role.models import Role
import datetime
from django.utils import timezone
import random
import string
import re
from .models import OTP

class UserRegistration(APIView):
    serializer_class = UserRegisterSerializer
    def post(self, request):
        request.body
        ser_data = self.serializer_class(data=request.data)
        role=Role.objects.get(name="user")
        ##handle otp    


class SendOTP(APIView):
    def generate_otp(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


    def validate_phone_number(self,phone_number: str):
        pattern = r"^0(9[1-9]{1}[0-9]{1})\d{7}$"  
        return bool(re.match(pattern, phone_number))

    def post(self, request):
        if request.data.get("phone_number") is None:
            return Response({"error":"send phone_number"},status=status.HTTP_400_BAD_REQUEST)
        phone_number=request.data["phone_number"]
        if self.validate_phone_number(phone_number) is False:
            return Response({"error":"phone number is not valid"},status=status.HTTP_400_BAD_REQUEST)
        code=self.generate_otp()
        if OTP.objects.filter(phone_number=phone_number,otp_for="login").exists():
            otp=OTP.objects.get(phone_number=phone_number,otp_for="login")
            num_try=((timezone.now()-otp.otp_expire-datetime.timedelta(minutes=2))/datetime.timedelta(minutes=20))
            print((num_try))
            if int(num_try)>0:
                all_try=int(num_try)+otp.max_try
            else:
                all_try=otp.max_try
            if all_try<=0:
                return Response({"error":"request limit,try 20 minute later"},status=status.HTTP_400_BAD_REQUEST)
            elif all_try>=3:
                otp.otp_code=code
                otp.max_try=2
                otp.otp_expire=timezone.now()+datetime.timedelta(minutes=2)
                otp.save()
            else:
                otp.otp_code=code
                otp.max_try=all_try-1
                otp.otp_expire=timezone.now()+datetime.timedelta(minutes=2)
                otp.save()
        else:
            OTP.objects.create(phone_number=phone_number,otp_for="login",otp_code=code,otp_expire=timezone.now() + datetime.timedelta(minutes=2),max_try=2)
            
        ## SMS HANDLING 
        return Response({"code":code},status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        pass


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST) 


