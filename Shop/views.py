from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from Shop.models import ShopRequest
from Shop.serializers import CreateShopRequestSerializer, ShopRequestSerializer
from Product.models import StaticField, ToplevelTopic, MidlevelTopic, LowlevelTopic, ProductTopic
from Product.serializers import GetFieldForCreateProductSerializer, GetFieldSerializer, ToplevelTopicSerializer, MidlevelTopicSerializer, LowlevelTopicSerializer, ProductTopicSerializer
# Create your views here.

class GetToplevelTopicView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if request.user.role.name!="shop_admin":
            return Response({"message":"You can not access this url"},status=status.HTTP_403_FORBIDDEN)
        if request.query_params.get("search_key") and request.query_params.get("search_key") != "":
            search_key = request.query_params.get("search_key")
            toplevel_topic = ToplevelTopic.objects.filter(name__icontains=search_key)
        else:
            toplevel_topic = ToplevelTopic.objects.all()
        if len(toplevel_topic)<=0:
            return Response({"message":"No toplevel topic found"},status=status.HTTP_404_NOT_FOUND)
        ser_data=ToplevelTopicSerializer(instance=toplevel_topic, many=True)
        return Response(ser_data.data,status=status.HTTP_200_OK)
        
        

class GetMidlevelTopicView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if request.user.role.name!="shop_admin":
            return Response({"message" :"You can not access this url"},status=status.HTTP_403_FORBIDDEN)
        if request.query_params.get("search_key") and request.query_params.get("search_key") != "":
            search_key = request.query_params.get("search_key")
            midlevel_topic = MidlevelTopic.objects.filter(name__icontains=search_key)
        else:
            midlevel_topic = MidlevelTopic.objects.all()
        if len(midlevel_topic)<=0:
            return Response({"message":"No midlevel topic found"},status=status.HTTP_404_NOT_FOUND)
        ser_data=MidlevelTopicSerializer(instance=midlevel_topic, many=True)
        return Response(ser_data.data,status=status.HTTP_200_OK)
        

class GetLowlevelTopicView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if request.user.role.name!="shop_admin":
            return Response({"message":"You can not access this url"},status=status.HTTP_403_FORBIDDEN)
        if request.query_params.get("search_key") and request.query_params.get("search_key") != "":
            search_key = request.query_params.get("search_key")
            lowlevel_topic = LowlevelTopic.objects.filter(name__icontains=search_key)
        else:
            lowlevel_topic = LowlevelTopic.objects.all()
        if len(lowlevel_topic)<=0:
            return Response({"message":"No lowlevel topic found"},status=status.HTTP_404_NOT_FOUND)
        ser_data=LowlevelTopicSerializer(instance=lowlevel_topic, many=True)
        return Response(ser_data.data,status=status.HTTP_200_OK)
    
    
class GetProductTopicView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if request.user.role.name!="shop_admin":
            return Response({"message":"You can not access this url"},status=status.HTTP_403_FORBIDDEN)
        if request.query_params.get("search_key") and request.query_params.get("search_key") != "":
            search_key = request.query_params.get("search_key")
            product_topic = ProductTopic.objects.filter(name__icontains=search_key)
        else:
            product_topic = ProductTopic.objects.all()
        if len(product_topic)<=0:
            return Response({"message":"No product topic found"},status=status.HTTP_404_NOT_FOUND)
        ser_data=ProductTopicSerializer(instance=product_topic, many=True)
        return Response(ser_data.data,status=status.HTTP_200_OK)


class GetFieldsForCreateProductView(APIView):

    def post(self,request):
        if request.user.role.name!="shop_admin":
            return Response({"message":"You can not access this url"},status=status.HTTP_403_FORBIDDEN)
        
        if not request.data.get("prouduct_topic_id"):
            return Response({"error":"send prouduct_topic_id"},status=status.HTTP_400_BAD_REQUEST)
        
        prouduct_topic=ProductTopic.objects.get(id=request.data.get("prouduct_topic_id"))
        lowlevel_topic=prouduct_topic.lowlevel_topic
        midlevel_topic=lowlevel_topic.midlevel_topic
        toplevel_topic=midlevel_topic.toplevel_topic
        from itertools import chain

        fields = chain(
            StaticField.objects.filter(topic_level=1, object_id=toplevel_topic.id),
            StaticField.objects.filter(topic_level=2, object_id=midlevel_topic.id),
            StaticField.objects.filter(topic_level=3, object_id=lowlevel_topic.id),
            StaticField.objects.filter(topic_level=4, object_id=prouduct_topic.id),
        )
        fields = list(fields)  # Convert chain object to list for serialization
        if not fields:
            return Response({"error":"there is not any fields"},status=status.HTTP_204_NO_CONTENT)
        return Response({"data":GetFieldForCreateProductSerializer(instance=fields, many=True).data})
    

    
class CreateShopRequestView(APIView):    
    def post(self,request):
        serializer = CreateShopRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Shop request created successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

