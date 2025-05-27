
import requests
from Bank.models import UserFacility,UserInstallment
from Bank.serializers import CancledFacilityUseerSerialiser, DoneFacilityUseerSerialiser, FacilityUseerSerialiser, InstallmentFacilityUseerSerialiser, UserInstallmentSerialiser
from Order.serializers import OrderSerializer
from Product.serializers import CartItemSerializer, CreateCartItemSerializer, ProductInstanceSerialiser, ProductSerialiser, AllProductInstanceSerializer
from Product.models import Product, ProductInstance
from Order.models import BoughtOrder, Cart, CartItem,Order
from User.models import CustomUser
from User.serializers import AddressProfileSerializer, AddressSerializer, ConfirmationSerializer, HomeSerializer, TempAdressSerializer, UserRegisterSerializer, UserWalletSerialiser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from EvaamBack import  settings
from Role.models import Role
import datetime
from django.utils import timezone
import random
import string
import re
from .models import OTP, CreditWallet,JibitToken,TempAddress,Address, UserCreditTransaction
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import jdatetime  


class SendOTP(APIView):
    def generate_otp(self):
        return ''.join(random.choices(string.digits, k=8))


    def validate_phone_number(self,phone_number: str):
        pattern = r"^0(9[0-9]{1}[0-9]{1})\d{7}$"  
        return bool(re.match(pattern, phone_number))

    def post(self, request):
        print(" \n \n REQUEST DATA \n \n: ", request.data)
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
            return Response({"message":"ارسال کد با خطایی مواجه شد."},status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def validate_phone_number(self,phone_number: str):
        pattern = r"^0(9[0-9]{1}[0-9]{1})\d{7}$"  
        return bool(re.match(pattern, phone_number))
    
    def post(self, request, *args, **kwargs):
        if request.data.get("phone_number") is None:
            return Response({"error":"send phone_number"},status=status.HTTP_400_BAD_REQUEST)
        phone_number=request.data["phone_number"]
        if not self.validate_phone_number(phone_number):
            return Response({"error":"phone number format is not valid"},status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("otp_code") is None:
            return Response({"error":"send otp code"},status=status.HTTP_400_BAD_REQUEST)
        if not OTP.objects.filter(phone_number=phone_number,otp_for="login").exists():
            return Response({"error":"first make an otp code for yourself"},status=status.HTTP_400_BAD_REQUEST)
        otp=OTP.objects.get(phone_number=phone_number,otp_for="login")
        if timezone.now()>otp.otp_expire:
            return Response({"error":"time of otp is expired"},status=status.HTTP_400_BAD_REQUEST)
        if otp.otp_code==request.data["otp_code"]:
            if CustomUser.objects.filter(phone_number=phone_number).exists():
                user=CustomUser.objects.get(phone_number=phone_number)
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
class SendSecondPhoneOTP(APIView):
    permission_classes = [IsAuthenticated]


    def generate_otp(self):
        return ''.join(random.choices(string.digits, k=8))
    
    def validate_phone_number(self,phone_number: str):
        pattern = r"^0(9[0-9]{1}[0-9]{1})\d{7}$"
        return bool(re.match(pattern, phone_number))
    
    def post(self, request):
        if request.data.get("second_phone_number") is None:
            return Response({"error":"send second_phone_number"},status=status.HTTP_400_BAD_REQUEST)
        if not self.validate_phone_number(request.data["second_phone_number"]):
            return Response({"error":"second phone number format is not valid"},status=status.HTTP_400_BAD_REQUEST)
        

        #!bug for_phone_number should add otp table 
        code=self.generate_otp()
        if OTP.objects.filter(phone_number=request.data["second_phone_number"],otp_for="second_phone").exists():
            otp=OTP.objects.get(phone_number=request.data["second_phone_number"],otp_for="second_phone")
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
            OTP.objects.create(phone_number=request.data["second_phone_number"],otp_for="second_phone",otp_code=code,otp_expire=timezone.now() + datetime.timedelta(minutes=2),max_try=2)
            
        ## SMS HANDLING 
        print(code)
        data = {'from': '50002710054854', 'to': request.data["second_phone_number"], 'text': f' شمارۀ {request.data["second_phone_number"] }، در پلتفرم ایوام به عنوان شمارۀ اضطراری، توسط صاحب شمارۀ  { request.user.phone_number}، ثبت گردیده است. لطفا کد زیر در اختیار صاحب شماره اول قرار دهید.\n {code}'}
        response = requests.post('https://console.melipayamak.com/api/send/simple/2d475adf0f3f4fa3bf59f1a99eed0712', json=data)
        if response.json()["status"]=="ارسال موفق بود":
            return Response({"message":"با موفقیت ارسال شد"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"ارسال کد با خطایی مواجه شد.","code":code},status=status.HTTP_400_BAD_REQUEST)
        

class ConfirmInformationView(APIView):
    permission_classes = [IsAuthenticated]
    def convert_shamsi_to_miladi(self,shamsi_date):
        array_of_date=shamsi_date.split("/")
        return jdatetime.date(int(array_of_date[0]),int(array_of_date[1]),int(array_of_date[2])).togregorian()

    
    def validate_phone_number(self,phone_number: str):
        pattern = r"^0(9[0-9]{1}[0-9]{1})\d{7}$"
        return bool(re.match(pattern, phone_number))

    def post(self, request):
        if request.user.confirmed_data:
            return Response({"error":"your information is already confirmed"},status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get("second_phone_number") is None:
            return Response({"error":"send second_phone_number"},status=status.HTTP_400_BAD_REQUEST)

        if not self.validate_phone_number(request.data["second_phone_number"]):
            return Response({"error":"phone number format is not valid"},status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get("otp_code") is None:
            return Response({"error":"send otp code"},status=status.HTTP_400_BAD_REQUEST)

        if not OTP.objects.filter(phone_number=request.data["second_phone_number"],otp_for="second_phone").exists():
            return Response({"error":"first make an otp code for yourself"},status=status.HTTP_400_BAD_REQUEST)
        
        otp=OTP.objects.get(phone_number=request.data["second_phone_number"],otp_for="second_phone")
        if timezone.now()>otp.otp_expire:
            return Response({"error":"time of otp is expired"},status=status.HTTP_400_BAD_REQUEST)
        if not otp.otp_code==request.data["otp_code"]:
            return Response({"error":"the code is wrong"},status=status.HTTP_400_BAD_REQUEST)
        second_phone_number=request.data["second_phone_number"]
        
        
        if JibitToken.objects.filter(created_at__gte=timezone.now()-datetime.timedelta(days=1)).exists():
            jibit_token=JibitToken.objects.get(created_at__gte=timezone.now()-datetime.timedelta(days=1))
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

        
        second_phone_path=f"https://napi.jibit.ir/ide/v1/services/matching?nationalCode={national_code}&mobileNumber={second_phone_number}"
        response_of_check_second_phone=requests.get(second_phone_path,headers=header)
        if 200<=response_of_check_second_phone.status_code<=299:
            if response_of_check_second_phone.json()["matched"]:
                return Response({"error":"your national_code and your second phone number is matched"},status=status.HTTP_400_BAD_REQUEST)

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
                        user.birthday_date=self.convert_shamsi_to_miladi(request.data.get("birthday_date"))
                        user.confirmed_data=True
                        user.second_phone_number=second_phone_number
                        user.shamsi_birthday_date=base_birthday_date
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
            jibit_token=JibitToken.objects.get(created_at__gte=timezone.now()-datetime.timedelta(days=1))
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
        
        if Address.objects.filter(user=request.user,postal_code=request.data["postal_code"]).exists():
            return Response({"error":"your address is already confirmed"},status=status.HTTP_400_BAD_REQUEST)
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
        confirmed_data=user.confirmed_data
        confirmed_address=user.confirmed_address
        if confirmed_data:
            data=ConfirmationSerializer(instance=user).data
        else:
            data=None
        
        if confirmed_address:
            if not Address.objects.filter(user=user).exists():
                confirmed_address=False
                address=None
            else:    
                address=AddressProfileSerializer(instance=Address.objects.filter(user=user).order_by("-created_at").first()).data
        else:
            address=None
        return Response({"data":data,"confirmed_data":confirmed_data,"confirmed_address":confirmed_address,"address_data":address},status=status.HTTP_200_OK)
    


class UserWalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        if CreditWallet.objects.filter(user=request.user).exists():
            user_wallet=CreditWallet.objects.get(user=request.user)
        else:
            user_wallet=CreditWallet.objects.create(user=request.user,balance=0.0)

        if UserCreditTransaction.objects.filter(credit_wallet=user_wallet).exists():
            transactions=UserCreditTransaction.objects.filter(credit_wallet=user_wallet).order_by("-created_at")
            ser_data=UserWalletSerialiser(instance=transactions,many=True)
            return Response({"data":ser_data.data,"wallet_balance":user_wallet.balance},status=status.HTTP_200_OK)
        else:
            return Response({"data":[],"wallet_balance":user_wallet.balance},status=status.HTTP_200_OK)

class MyFacilityView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self,request):
        cancled_instance=UserFacility.objects.filter(user=request.user,status="cancled")
        in_progress_instance=UserFacility.objects.filter(user=request.user,status="in_progress")
        installment_instance=UserFacility.objects.filter(user=request.user,status="installment")
        done_instance=UserFacility.objects.filter(user=request.user,status="done")
        if cancled_instance:
            cancled_ser_data=CancledFacilityUseerSerialiser(instance=cancled_instance,many=True).data
        else:
            cancled_ser_data=None
        if in_progress_instance:
            in_progress_ser_data = FacilityUseerSerialiser(instance=in_progress_instance, many=True).data
        else:
            in_progress_ser_data = None

        if installment_instance:
            installment_ser_data = InstallmentFacilityUseerSerialiser(instance=installment_instance, many=True).data
        else:
            installment_ser_data = None

        if done_instance:
            done_ser_data = DoneFacilityUseerSerialiser(instance=done_instance, many=True).data
        else:
            done_ser_data = None

        return Response({
            "canceled": cancled_ser_data,
            "in_progress": in_progress_ser_data,
            "installment": installment_ser_data,
            "done": done_ser_data
        }, status=status.HTTP_200_OK)


class MyInstallmentView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self,request): 
        if not UserFacility.objects.filter(user=request.user,status="installment").exists():
            return Response({"error":"you dont have any installment"},status=status.HTTP_400_BAD_REQUEST)
        installment_instance=UserFacility.objects.get(user=request.user,status="installment")
        not_paid_instance=UserInstallment.objects.filter(user_facility=installment_instance,is_paid=False,status="not_paid")
        paid_instance=UserInstallment.objects.filter(user_facility=installment_instance,is_paid=True,status="paid")
        if not_paid_instance:
            not_paid_data=UserInstallmentSerialiser(instance=not_paid_instance,many=True).data
        else:
            not_paid_data=None

        if paid_instance:
            paid_data=UserInstallmentSerialiser(instance=paid_instance,many=True).data
        else:
            paid_data=None

        return Response({"paid":paid_data,"not_piad":not_paid_data},status=status.HTTP_200_OK)

class MyCartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request): 
        if Cart.objects.filter(user=request.user).exists():
            cart=Cart.objects.get(user=request.user)
            cart_items=CartItem.objects.filter(cart=cart)
            if not cart_items:
                return Response({"data":[]},status=status.HTTP_200_OK)
            return Response({"data":CartItemSerializer(instance=cart_items,many=True, context={"request":request}).data},status=status.HTTP_200_OK)
        else:
            Cart.objects.create(user=request.user)
            return Response({"data":[]},status=status.HTTP_200_OK)
        
class AddProductsToCardView(APIView):
    permission_classes = [IsAuthenticated]
    def post(seld,request): 
        if Cart.objects.filter(user=request.user).exists():
            cart=Cart.objects.get(user=request.user)
        else:
            cart=Cart.objects.create(user=request.user)

        if request.data.get("product_instances") is None:
            return Response({"error":"send product_instances"},status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(request.data.get("product_instances"),list):
            return Response({"error":"product_instances must be a list"})
        product_instances=request.data["product_instances"]
        new_product_instance=[]

        for product_instance in product_instances:
            product_instance["cart"]=cart.id

            if product_instance.get("product_instance") is None:
                return Response({"error":"send product instance product_instance"},status=status.HTTP_400_BAD_REQUEST)
            if product_instance.get("quantity") is None:
                return Response({"error":"send quantity"},status=status.HTTP_400_BAD_REQUEST)
            if product_instance.get("quantity")<1:
                return Response({"error":"quantity must be greater than 0"},status=status.HTTP_400_BAD_REQUEST)

            if ProductInstance.objects.filter(id=product_instance["product_instance"]).exists()==False:
                return Response({"error":f"product instance with product_instance {product_instance['product_instance']} does not exist"},status=status.HTTP_400_BAD_REQUEST)
            if CartItem.objects.filter(cart=cart,product_instance__id=product_instance["product_instance"]).exists():
                cart_item=CartItem.objects.get(cart=cart,product_instance__id=product_instance["product_instance"])
                cart_item.quantity+=product_instance["quantity"]
                cart_item.save()
            else:
                new_product_instance.append(product_instance)

        ser_data=CreateCartItemSerializer(data=new_product_instance,many=True)
        if ser_data.is_valid(raise_exception=True):
            ser_data.save()
            return Response({"message": "Products added to cart successfully"}, status=status.HTTP_200_OK)            

        else:
            return Response({"error":"serializer is not valid"},status=status.HTTP_400_BAD_REQUEST)


class ReplaceCartCardView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        if Cart.objects.filter(user=request.user).exists():
            cart = Cart.objects.get(user=request.user)
        else:
            cart = Cart.objects.create(user=request.user)

        if request.data.get("product_instances") is None:
            return Response({"error":"send product_instances"},status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(request.data.get("product_instances"),list):
            return Response({"error":"product_instances must be a list"})
        product_instances=request.data["product_instances"]

        for product_instance in product_instances:
            product_instance["cart"]=cart.id

            if product_instance.get("product_instance") is None:
                return Response({"error":"send product instance product_instance"},status=status.HTTP_400_BAD_REQUEST)
            if product_instance.get("quantity") is None:
                return Response({"error":"send quantity"},status=status.HTTP_400_BAD_REQUEST)
            if product_instance.get("quantity")<1:
                return Response({"error":"quantity must be greater than 0"},status=status.HTTP_400_BAD_REQUEST)

            if ProductInstance.objects.filter(id=product_instance["product_instance"]).exists()==False:
                return Response({"error":f"product instance with product_instance {product_instance['product_instance']} does not exist"},status=status.HTTP_400_BAD_REQUEST)
            

        ser_data=CreateCartItemSerializer(data=product_instances,many=True)
        if ser_data.is_valid(raise_exception=True):
            CartItem.objects.filter(cart=cart.id).delete() 
            ser_data.save()
            return Response({"message": "Products added to cart successfully"}, status=status.HTTP_200_OK)            

        else:
            return Response({"error":"serializer is not valid"},status=status.HTTP_400_BAD_REQUEST)
    
class BuyProductView(APIView):
    permission_classes = [IsAuthenticated]
    def final_cost(self,cost,percent,quantity):
        
        return quantity*(cost - (cost * percent / 100))
    
    def post(self,request):
        user=request.user

        if request.data.get("otp_code") is None:
            return Response({"error":"send otp code"},status=status.HTTP_400_BAD_REQUEST)
        if not OTP.objects.filter(phone_number=user.phone_number,otp_for="buy_product").exists():
            return Response({"error":"first make an otp code for yourself"},status=status.HTTP_400_BAD_REQUEST)
        otp=OTP.objects.get(phone_number=user.phone_number,otp_for="buy_product")
        if timezone.now()>otp.otp_expire:
            return Response({"error":"time of otp is expired"},status=status.HTTP_400_BAD_REQUEST)
        if otp.otp_code!=request.data["otp_code"]:
            return Response({"error":"the code is wrong"},status=status.HTTP_400_BAD_REQUEST)
        
        if Cart.objects.filter(user=request.user).exists():
            cart = Cart.objects.get(user=request.user)
        else:
            cart = Cart.objects.create(user=request.user)


        product_items=CartItem.objects.filter(cart=cart)
        if not product_items:
            return Response({"erroe":"your cart is empty"},status=status.HTTP_400_BAD_REQUEST)
        all_cost=0
        num_of_product=0
        for product_item in product_items:
            all_cost+=self.final_cost(product_item.product_instance.price,product_item.product_instance.discount,product_item.quantity)
            num_of_product+=product_item.quantity
        wallet=CreditWallet.objects.get_or_create(user=request.user)[0]
        if wallet.balance<all_cost:
            return Response({"error":"your balance is not enough"},status=status.HTTP_400_BAD_REQUEST)
        wallet.balance-=all_cost
        wallet.save()
        tranasction=UserCreditTransaction.objects.create(credit_wallet=wallet,
                                                value=all_cost,
                                                type="bought",
                                                is_booster=False
                                                )
        
        if not Address.objects.filter(user=request.user).exists():
            return Response({"error": "No address found for the user"}, status=status.HTTP_400_BAD_REQUEST)
        
        address = Address.objects.filter(user=request.user).order_by("-created_at").first()

        order = Order.objects.create(
            user=request.user,
            all_price=all_cost,
            delivery_price=0,  
            status="paid",
            transaction=tranasction,  
            num_of_product=num_of_product,
            is_paid=True,
            address=address
        )
        for product_item in product_items:
                BoughtOrder.objects.create(
                user=request.user,
                product_intance=product_item.product_instance,
                order=order,
                product_discount=product_item.product_instance.discount,
                all_discount=0,  
                product_cost=product_item.product_instance.price,
                quantity=product_item.quantity,
                paid_cost=self.final_cost(product_item.product_instance.price, product_item.product_instance.discount, product_item.quantity),
            )

        CartItem.objects.filter(cart=cart).delete()

        return Response({"message":"your bought is done"},status=status.HTTP_200_OK)
        
class MyOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        if not orders.exists():
            return Response({"error": "No orders found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"orders": OrderSerializer(instance=orders,many=True).data}, status=status.HTTP_200_OK)




class PayInstallmentVeiw(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        if UserFacility.objects.filter(user=request.user,status="installment").exists()==False:
            return Response({"error":"you dont have any installment"},status=status.HTTP_400_BAD_REQUEST)
        sent_installment_id=request.data.get("installment_id")
        if not sent_installment_id:
            return Response({"error":"send valid installment_id"},status=status.HTTP_400_BAD_REQUEST)
        if UserInstallment.objects.filter(user_facility__user=request.user,id=sent_installment_id,user_facility__status="installment").exists() == False:
            return Response({"error":"installment not matched"},status=status.HTTP_400_BAD_REQUEST)
        installmenty_should_pay= UserInstallment.objects.filter(user_facility__user=request.user,user_facility__status="installment",is_paid=False).order_by("installment_number").first()
        sent_installment=UserInstallment.objects.get(id=sent_installment_id)
        if sent_installment.is_paid:
            return Response({"error":"you piad it before"},status=status.HTTP_400_BAD_REQUEST)
        if installmenty_should_pay.id !=sent_installment.id:
            return Response({"error":f"you should pay insatellment {installmenty_should_pay.installment_number} first"},status=status.HTTP_400_BAD_REQUEST)
        last_install_ment=UserInstallment.objects.filter(user_facility__user=request.user,user_facility__status="installment",is_paid=False).order_by("-installment_number").first()

        sent_installment.is_paid=True
        sent_installment.status="paid"
        sent_installment.paid_date=datetime.datetime.now().date()
        sent_installment.save() 
        
        if last_install_ment.id==sent_installment.id :
            last_install_ment.user_facility.status="done"
            last_install_ment.user_facility.save()
        return Response({"message":"installment is paid"},status=status.HTTP_200_OK)

    

class GetCartCostView(APIView):
    permission_classes = [IsAuthenticated]
    def final_cost(self,cost,percent,quantity):
        
        return quantity*(cost - (cost * percent / 100))
    
    def get(self,request):
        if Cart.objects.filter(user=request.user).exists():
            cart = Cart.objects.get(user=request.user)
        else:
            cart = Cart.objects.create(user=request.user)

        product_items=CartItem.objects.filter(cart=cart)
        if not product_items:
            return Response({"erroe":"your cart is empty"},status=status.HTTP_400_BAD_REQUEST)
        cost=0
        for product_item in product_items:
            cost+=self.final_cost(product_item.product_instance.price,product_item.product_instance.discount,product_item.quantity)
        return Response({"all_products_cost":cost},status=status.HTTP_200_OK)



class SingleiInstallmentView(APIView):

    permission_classes = [IsAuthenticated]
    def post(self,request):
        if not request.data.get("installment_id"):
            return Response({"error":"please send installment_id"})
        installment_id=request.data.get("installment_id")
        installment=UserInstallment.objects.get(id=installment_id)
        if installment.user_facility.user != request.user:
            return Response({"error":"this installment is not yours"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"data":UserInstallmentSerialiser(instance=installment).data},status=status.HTTP_200_OK)
    
class PaymentOTPVeiw(APIView):
    permission_classes = [IsAuthenticated]
    def final_cost(self,cost,percent,quantity):
        return quantity*(cost - (cost * percent / 100))
    
    def generate_otp(self):
        return ''.join(random.choices(string.digits, k=8))
    
    def post(self,request):
        if Cart.objects.filter(user=request.user).exists():
            cart= Cart.objects.get(user=request.user)
        else:
            cart=Cart.objects.create(user=request.user)

        product_items=CartItem.objects.filter(cart=cart)
        if not product_items:
            return Response({"erroe":"your cart is empty"},status=status.HTTP_400_BAD_REQUEST)
        cost=0
        for product_item in product_items:
            cost+=self.final_cost(product_item.product_instance.price,product_item.product_instance.discount,product_item.quantity)
        wallet=CreditWallet.objects.get_or_create(user=request.user)[0]
        if wallet.balance<cost:
            return Response({"error":"your balance is not enough"},status=status.HTTP_400_BAD_REQUEST)
        user=request.user
        code=self.generate_otp()
        if OTP.objects.filter(phone_number=user.phone_number,otp_for="buy_product").exists():
            otp=OTP.objects.get(phone_number=user.phone_number,otp_for="buy_product")
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
            OTP.objects.create(phone_number=user.phone_number,otp_for="buy_product",otp_code=code,otp_expire=timezone.now() + datetime.timedelta(minutes=2),max_try=2)
            
        ## SMS HANDLING 
        str_cost=str(cost)
        str_cost = str_cost.replace(".", ",")  # Replace '.' with ',' for Persian format
        print(str_cost)

        data = {'from': '50002710054854', 'to': user.phone_number, 'text': f'کد خرید از ایوام \nوارد کردن این کد به منزله تخلیه کیف پول شما میباشد. \nمبلغ:{str_cost} \n کد:{code}'}
        response = requests.post('https://console.melipayamak.com/api/send/simple/2d475adf0f3f4fa3bf59f1a99eed0712', json=data)
        if response.json()["status"]=="ارسال موفق بود":
            return Response({"message":"با موفقیت ارسال شد"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"ارسال کد با خطایی مواجه شد."},status=status.HTTP_400_BAD_REQUEST) 
        

        
