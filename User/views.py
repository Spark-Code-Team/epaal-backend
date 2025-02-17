
from User.models import CustomUser
from User.serializers import HomeSerializer, UserRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
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
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

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
        if not self.validate_phone_number(phone_number) :
            return Response({"error":"phone number format is not valid"},status=status.HTTP_400_BAD_REQUEST)
        code=self.generate_otp()
        if OTP.objects.filter(phone_number=phone_number,otp_for="login").exists():
            otp=OTP.objects.get(phone_number=phone_number,otp_for="login")
            num_try=((timezone.now()-otp.otp_expire-datetime.timedelta(minutes=2))/datetime.timedelta(minutes=20))
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
    def validate_phone_number(self,phone_number: str):
        pattern = r"^0(9[1-9]{1}[0-9]{1})\d{7}$"  
        return bool(re.match(pattern, phone_number))
    
    def post(self, request, *args, **kwargs):
        if request.data.get("phone_number") is None:
            return Response({"error":"send phone_number"},status=status.HTTP_400_BAD_REQUEST)
        if not self.validate_phone_number(request.data["phone_number"]):
            return Response({"error":"phone number format is not valid"},status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("otp_code") is None:
            return Response({"error":"send otp code"},status=status.HTTP_400_BAD_REQUEST)
        if not OTP.objects.filter(phone_number=request.data["phone_number"],otp_for="login").exists():
            return Response({"error":"first make an otp code for yourself"},status=status.HTTP_400_BAD_REQUEST)
        otp=OTP.objects.get(phone_number=request.data["phone_number"],otp_for="login")
        if timezone.now()>otp.otp_expire:
            return Response({"error":"time of otp is expired"},status=status.HTTP_400_BAD_REQUEST)
        if otp.otp_code==request.data["otp_code"]:
            if CustomUser.objects.filter(phone_number=request.data["phone_number"]).exists():
                user=CustomUser.objects.get(phone_number=request.data["phone_number"])
                if user.has_two_factor:
                    if request.data.get("password") is None:
                        return Response({"two_factor":True,'refresh':None,'access':None},status=status.HTTP_406_NOT_ACCEPTABLE)
                    else:
                        if user.check_password(request.data["password"]):
                            refresh=RefreshToken.for_user(user=user)
                            return Response({"two_factor":None,'refresh':str(refresh),'access':str(refresh.access_token)},status=status.HTTP_200_OK)
                        else:
                            return  Response({"error":"password is not valid"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    refresh=RefreshToken.for_user(user=user)
                    return Response({"two_factor":None
                                ,'refresh':str(refresh),
                                'access':str(refresh.access_token)},status=status.HTTP_200_OK)

            else:
                user=CustomUser.objects.create(phone_number=request.data["phone_number"],role=Role.objects.get(name="user"))
                refresh=RefreshToken.for_user(user=user)
                return Response({"two_factor":None
                                ,'refresh':str(refresh),
                                'access':str(refresh.access_token)},status=status.HTTP_200_OK)
        else:
            return Response({"error":"the code is wrong"},status=status.HTTP_400_BAD_REQUEST)



        


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST) 


class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ser_data=HomeSerializer(instance=request.user)
        return Response(ser_data.data,status=status.HTTP_200_OK)

