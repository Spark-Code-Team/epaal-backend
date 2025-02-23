
import requests
from User.models import CustomUser
from User.serializers import AddressSerializer, ConfirmationSerializer, HomeSerializer, TempAdressSerializer, UserRegisterSerializer
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
from .models import OTP,JibitToken,TempAddress,Address
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
        return ''.join(random.choices(string.digits, k=8))


    def validate_phone_number(self,phone_number: str):
        pattern = r"^0(9[0-9]{1}[0-9]{1})\d{7}$"  
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
        print(code)
        data = {'from': '50002710054854', 'to': request.data["phone_number"], 'text': f'کدِ ورود شما به ایوام \n {code}'}
        response = requests.post('https://console.melipayamak.com/api/send/simple/2d475adf0f3f4fa3bf59f1a99eed0712', json=data)
        if response.json()["status"]=="ارسال موفق بود":
            return Response({"message":"با موفقیت ارسال شد"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"ارسال کد با خطایی مواجه شد.","code":code},status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def validate_phone_number(self,phone_number: str):
        pattern = r"^0(9[1-9]{1}[0-9]{1})\d{7}$"  
        return bool(re.match(pattern, phone_number))
    
    def post(self, request, *args, **kwargs):
        if request.data.get("phone_number") is None:
            return Response({"error":"send phone_number"},status=status.HTTP_400_BAD_REQUEST)
        # if not self.validate_phone_number(request.data["phone_number"]):
        #     return Response({"error":"phone number format is not valid"},status=status.HTTP_400_BAD_REQUEST)
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

class ConfirmInformationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.confirmed_data:
            return Response({"error":"your information is already confirmed"},status=status.HTTP_400_BAD_REQUEST)
        
        if JibitToken.objects.filter(created_at__gte=timezone.now()-datetime.timedelta(days=1)).exists():
            jibit_token=JibitToken.objects.get(created_at__gte=timezone.now()-datetime.timedelta(days=24))
            access_token=jibit_token.access_token
        else:
            response = requests.post('https://napi.jibit.ir/ide/v1/tokens/generate', json={"apiKey":"cvYDi4nzvP","secretKey":"5Ioyhh9MDbjA19_JQi16CJWI9"})
            JibitToken.objects.create(access_token=response.json()["accessToken"],refresh_token=response.json()["refreshToken"])
            access_token=response.json()["accessToken"]
        
        header={"Authorization":f"Bearer {access_token}"}
        if request.data.get("first_name") is None:
            return Response({"error":"send first_name"},status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("last_name") is None:
            return Response({"error":"send last_name"},status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("national_code") is None:
            return Response({"error":"send national_code"},status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("birthday_date") is None:
            return Response({"error":"send birthday_date"},status=status.HTTP_400_BAD_REQUEST)
        phone_number=request.user.phone_number
        first_name=request.data.get("first_name")
        last_name=request.data.get("last_name")
        national_code=request.data.get("national_code")
        base_birthday_date=request.data.get("birthday_date").replace("/","-")
        birthday_date=request.data.get("birthday_date").replace("/","")
        path=f"https://napi.jibit.ir/ide/v1/services/matching?nationalCode={national_code}&mobileNumber={phone_number}"
        response_of_check_national_code_mobile=requests.get(path,headers=header)
        if 200<=response_of_check_national_code_mobile.status_code<=299:
            if response_of_check_national_code_mobile.json()["matched"]:
                path2=f"https://napi.jibit.ir/ide/v1/services/identity/similarity?nationalCode={national_code}&birthDate={birthday_date}&firstName={first_name}&lastName={last_name}"
                response_of_check_information=requests.get(path2,headers=header)
                if 200<=response_of_check_information.status_code<=299:
                    if response_of_check_information.json()["lastNameSimilarityPercentage"]==100 and response_of_check_information.json()["firstNameSimilarityPercentage"]==100:  
                        user=request.user
                        user.first_name=first_name
                        user.last_name=last_name
                        user.national_code=national_code
                        user.birthday_date=base_birthday_date
                        user.confirmed_data=True
                        user.save()
                        return Response({"message":"your validation is done","data":ConfirmationSerializer(instance=request.user).data},status=status.HTTP_200_OK)
                    else:
                        return Response({"error":"your information is not matched"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(response_of_check_information.json(),status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":"your national_code and your phonr number is not matched"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response_of_check_national_code_mobile.json(),status=status.HTTP_400_BAD_REQUEST)
        

class ShowAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.data.get("postal_code") is None:
            return Response({"error":"send postal_code"},status=status.HTTP_400_BAD_REQUEST)
        if len(request.data.get("postal_code"))!=10:    
            return Response({"error":"postal_code must be 10 characters"},status=status.HTTP_400_BAD_REQUEST)
        
        postal_code=request.data.get("postal_code")
        if JibitToken.objects.filter(created_at__gte=timezone.now()-datetime.timedelta(days=1)).exists():
            jibit_token=JibitToken.objects.get(created_at__gte=timezone.now()-datetime.timedelta(days=24))
            access_token=jibit_token.access_token
        else:
            response = requests.post('https://napi.jibit.ir/ide/v1/tokens/generate', json={"apiKey":"cvYDi4nzvP","secretKey":"5Ioyhh9MDbjA19_JQi16CJWI9"})
            JibitToken.objects.create(access_token=response.json()["accessToken"],refresh_token=response.json()["refreshToken"])
            access_token=response.json()["accessToken"]
        header={"Authorization":f"Bearer {access_token}"}
        path=f"https://napi.jibit.ir/ide//v1/services/postal?code={postal_code}"
        response_of_check_postal_code=requests.get(path,headers=header)
        if 200<=response_of_check_postal_code.status_code<=299:
            temp_address=TempAddress.objects.create(postal_code=postal_code,address=response_of_check_postal_code.json()["addressInfo"]["address"])    
            return Response(TempAdressSerializer(instance=temp_address).data,status=status.HTTP_200_OK)
        else:
            return Response(response_of_check_postal_code.json(),status=status.HTTP_400_BAD_REQUEST)
        

class ConfirmAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.data.get("postal_code") is None:
            return Response({"error":"send postal_code"},status=status.HTTP_400_BAD_REQUEST)
        
        if len(request.data.get("postal_code"))!=10:
            return Response({"error":"postal_code must be 10 characters"},status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get("id") is None:
            return Response({"error":"send id"},status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get("address") is None:
            return Response({"error":"send address"},status=status.HTTP_400_BAD_REQUEST)
        
        if not TempAddress.objects.filter(id=request.data["id"],postal_code=request.data["postal_code"],address=request.data["address"]).exists():
            return Response({"error":"the address is not valid"},status=status.HTTP_400_BAD_REQUEST)
        address=TempAddress.objects.get(id=request.data["id"],postal_code=request.data["postal_code"],address=request.data["address"])
        user=request.user
        user.confirmed_address=True
        user.save()
        if not Address.objects.filter(address=address.address,postal_code=address.postal_code,user=user).exists():
            user_adress=Address.objects.create(address=address.address,postal_code=address.postal_code,user=user)
        else:
            user_adress=Address.objects.get(address=address.address,postal_code=address.postal_code)
        return Response({"message":"your address is confirmed","data":AddressSerializer(instance=user_adress).data},status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user=request.user
        if user.confirmed_data:
            return Response({"data":ConfirmationSerializer(instance=user).data,"confirmed_data":True},status=status.HTTP_200_OK)
        else:
            return Response({"data":None,"confirmed_data":False},status=status.HTTP_400_BAD_REQUEST)