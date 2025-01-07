from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import All_ToplevelSerializer,ToplevelTopicSerializer,MidlevelTopicSerializer,ProductTopicSerializer,LowlevelTopicSerializer
from .models import MidlevelTopic, ProductTopic, ToplevelTopic , LowlevelTopic
from rest_framework.parsers import MultiPartParser

# Create your views here.

class ALLCategoryView(APIView):
    def get(self, request):
        if ToplevelTopic.objects.filter().exists():
            ser_data=All_ToplevelSerializer(instance=ToplevelTopic.objects.filter(),many=True)
            return Response({"toplevel_topic":ser_data.data},status=status.HTTP_200_OK)
        else:
            return Response({"error":"there is not any top level topic"},status=status.HTTP_204_NO_CONTENT)
        
class ShopLandingView(APIView):
    def get(self, request):
        pass
        

class CreateToplevelTopicView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser]

    def post(self, request):
        if request.user.role.name !="admin":
            return Response({"error":"you cant do this"},status=status.HTTP_400_BAD_REQUEST)
        ser_data=ToplevelTopicSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response({"message":"created","data":ser_data.data},status=status.HTTP_200_OK)
        else:
            return Response({"error":ser_data.errors},status=status.HTTP_400_BAD_REQUEST)

class CreateMidlevelTopicView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser]

    def post(self, request):
        if request.user.role.name !="admin":
            return Response({"error":"you cant do this"},status=status.HTTP_400_BAD_REQUEST)
        ser_data=MidlevelTopicSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response({"message":"created","data":ser_data.data},status=status.HTTP_200_OK)
        else:
            return Response({"error":ser_data.errors},status=status.HTTP_400_BAD_REQUEST)
        
class CreateLowLevelTopicView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser]

    def post(self, request):
        if request.user.role.name !="admin":
            return Response({"error":"you cant do this"},status=status.HTTP_400_BAD_REQUEST)
        ser_data=LowlevelTopicSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response({"message":"created","data":ser_data.data},status=status.HTTP_200_OK)
        else:
            return Response({"error":ser_data.errors},status=status.HTTP_400_BAD_REQUEST)

class CreateProductTopicView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser]

    def post(self, request):
        if request.user.role.name !="admin":
            return Response({"error":"you cant do this"},status=status.HTTP_400_BAD_REQUEST)
        ser_data=ProductTopicSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response({"message":"created","data":ser_data.data},status=status.HTTP_200_OK)
        else:
            return Response({"error":ser_data.errors},status=status.HTTP_400_BAD_REQUEST)
        
class GetToplevelTopicView(APIView):     
    def get(self,request):
        objects=ToplevelTopic.objects.filter()
        if len(objects)>0:
            ser_data=ToplevelTopicSerializer(instance=objects,many=True)
            return Response({"data":ser_data.data},status=status.HTTP_200_OK)
        else:
            return Response({"error":"there is not any topic"},status=status.HTTP_204_NO_CONTENT)




class GetMidlevelTopicView(APIView):     
    def get(self,request):
        objects=MidlevelTopic.objects.filter()
        if len(objects)>0:
            ser_data=MidlevelTopicSerializer(instance=objects,many=True)
            return Response({"data":ser_data.data},status=status.HTTP_200_OK)
        else:
            return Response({"error":"there is not any topic"},status=status.HTTP_204_NO_CONTENT)
        

class GetLowlevelTopicView(APIView):     
    def get(self,request):
        objects=LowlevelTopic.objects.filter()
        if len(objects)>0:
            ser_data=LowlevelTopicSerializer(instance=objects,many=True)
            return Response({"data":ser_data.data},status=status.HTTP_200_OK)
        else:
            return Response({"error":"there is not any topic"},status=status.HTTP_204_NO_CONTENT)


class GetProductTopicView(APIView):     
    def get(self,request):
        objects=ProductTopic.objects.filter()
        if len(objects)>0:
            ser_data=ProductTopicSerializer(instance=objects,many=True)
            return Response({"data":ser_data.data},status=status.HTTP_200_OK)
        else:
            return Response({"error":"there is not any topic"},status=status.HTTP_204_NO_CONTENT)
