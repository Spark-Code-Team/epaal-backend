
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

class UserRegistration(APIView):
    serializer_class = UserRegisterSerializer
    def post(self, request):
        request.body
        ser_data = self.serializer_class(data=request.data)
        role=Role.objects.get(name="user")
        ##handle otp    



class CustomTokenObtainPairView(TokenObtainPairView):
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


