from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import All_ToplevelSerializer,ToplevelTopicSerializer,MidlevelTopicSerializer,ProductTopicSerializer,LowlevelTopicSerializer,CreateFieldSerializer,GetFieldSerializer,Product
from .models import MidlevelTopic, ProductTopic, StaticField, ToplevelTopic , LowlevelTopic
from rest_framework.parsers import MultiPartParser
from django.contrib.contenttypes.models import ContentType

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
class DeleteToplevelTopicView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self,request):
        if request.user.role.name !="admin":
            return Response({"error":"you cant do this"},status=status.HTTP_400_BAD_REQUEST)
        if (request.data.get("toplevel_topic") is None) or (request.data["toplevel_topic"] is ""):
            return Response({"error":"you should send toplevel_topic"},status=status.HTTP_400_BAD_REQUEST)
        if ToplevelTopic.objects.filter(id=request.data["toplevel_topic"]).exists():
            ToplevelTopic.objects.get(id=request.data["toplevel_topic"]).delete()
            return Response({"message":"deleted"},status=status.HTTP_200_OK)
        else:
            return Response({"error":"toplevel with this id is not found"},status=status.HTTP_400_BAD_REQUEST)

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
        
class DeleteMidlevelTopicView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self,request):
        if request.user.role.name !="admin":
            return Response({"error":"you cant do this"},status=status.HTTP_400_BAD_REQUEST)
        if (request.data.get("midlevel_topic") is None) or (request.data["midlevel_topic"] is ""):
            return Response({"error":"you should send midlevel_topic"},status=status.HTTP_400_BAD_REQUEST)
        if MidlevelTopic.objects.filter(id=request.data["midlevel_topic"]).exists():
            MidlevelTopic.objects.get(id=request.data["midlevel_topic"]).delete()
            return Response({"message":"deleted"},status=status.HTTP_200_OK)
        else:
            return Response({"error":"midlevel with this id is not found"},status=status.HTTP_400_BAD_REQUEST)
        
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

class DeleteLowlevelTopicView(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self,request):
        if request.user.role.name !="admin":
            return Response({"error":"you cant do this"},status=status.HTTP_400_BAD_REQUEST)
        if (request.data.get("lowlevel_topic") is None) or (request.data["lowlevel_topic"] is ""):
            return Response({"error":"you should send lowlevel_topic"},status=status.HTTP_400_BAD_REQUEST)
        if LowlevelTopic.objects.filter(id=request.data["lowlevel_topic"]).exists():
            LowlevelTopic.objects.get(id=request.data["lowlevel_topic"]).delete()
            return Response({"message":"deleted"},status=status.HTTP_200_OK)
        else:
            return Response({"error":"lowlevel with this id is not found"},status=status.HTTP_400_BAD_REQUEST)

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
class DeleteProductTopicView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self,request):
        if request.user.role.name !="admin":
            return Response({"error":"you cant do this"},status=status.HTTP_400_BAD_REQUEST)
        if (request.data.get("product_topic") is None) or (request.data["product_topic"] is ""):
            return Response({"error":"you should send product_topic"},status=status.HTTP_400_BAD_REQUEST)
        if ProductTopic.objects.filter(id=request.data["product_topic"]).exists():
            ProductTopic.objects.get(id=request.data["product_topic"]).delete()
            return Response({"message":"deleted"},status=status.HTTP_200_OK)
        else:
            return Response({"error":"product with this id is not found"},status=status.HTTP_400_BAD_REQUEST)
        
class GetAllToplevelTopicView(APIView):     
    def post(self,request):
        objects=ToplevelTopic.objects.filter()
        if len(objects)>0:
            ser_data=ToplevelTopicSerializer(instance=objects,many=True)
            return Response({"data":ser_data.data},status=status.HTTP_200_OK)
        else:
            return Response({"error":"there is not any topic"},status=status.HTTP_204_NO_CONTENT)




class GetAllMidlevelTopicView(APIView):     
    def get(self,request):
        objects=MidlevelTopic.objects.filter()
        if len(objects)>0:
            ser_data=MidlevelTopicSerializer(instance=objects,many=True)
            return Response({"data":ser_data.data},status=status.HTTP_200_OK)
        else:
            return Response({"error":"there is not any topic"},status=status.HTTP_204_NO_CONTENT)
        

class GetAllLowlevelTopicView(APIView):     
    def post(self,request):
        filter_kwargs={}
        if(request.data.get("midlevel_topic") is not None) and( request.data["midlevel_topic"] is not ""):
            filter_kwargs["midlevel_topic"] = request.data["midlevel_topic"]
        objects=LowlevelTopic.objects.filter(**filter_kwargs)
        if len(objects)>0:
            ser_data=LowlevelTopicSerializer(instance=objects,many=True)
            return Response({"data":ser_data.data},status=status.HTTP_200_OK)
        else:
            return Response({"error":"there is not any topic"},status=status.HTTP_204_NO_CONTENT)


class GetAllProductTopicView(APIView):     
    def post(self,request):
        filter_kwargs={}
        if(request.data.get("lowlevel_topic") is not None) and( request.data["lowlevel_topic"] is not ""):
            filter_kwargs["lowlevel_topic"] = request.data["lowlevel_topic"]
        objects=ProductTopic.objects.filter(**filter_kwargs)
        if len(objects)>0:
            ser_data=ProductTopicSerializer(instance=objects,many=True)
            return Response({"data":ser_data.data},status=status.HTTP_200_OK)
        else:
            return Response({"error":"there is not any topic"},status=status.HTTP_204_NO_CONTENT)



class CreateFieldTopicView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.user.role.name !="admin":
            return Response({"error":"you cant do this"},status=status.HTTP_400_BAD_REQUEST)
        if (request.data.get("topic_level") is None) or (request.data["topic_level"] not in [1,2,3]):
            return Response({"error":"you should send topic_level by value 1,2 or 3"},status=status.HTTP_400_BAD_REQUEST)
        if (request.data.get("object_id") is None):
            return Response({"error":"you should send object_id"},status=status.HTTP_400_BAD_REQUEST)
        got_topic=request.data["topic_level"]
        topic_id=request.data["object_id"]
        if request.data.get("is_filter") is not None and request.data["is_filter"] in [True,False]:
            is_filter=request.data["is_filter"]
        else:
            is_filter=False
        if request.data.get("is_choosable") is not None and request.data["is_choosable"] in [True,False]:
            is_choosable=request.data["is_choosable"]
        else:
            is_choosable=False
        request.data["is_choosable"]=is_choosable
        request.data["is_filter"]=is_filter
        
        if got_topic == 2:
            if not MidlevelTopic.objects.filter(id=topic_id).exists():
                return Response({"error":"midlevel with this id is not found"},status=status.HTTP_400_BAD_REQUEST)

        elif got_topic == 3:
            if not LowlevelTopic.objects.filter(id=topic_id).exists():
                return Response({"error":"lowlevel with this id is not found"},status=status.HTTP_400_BAD_REQUEST)

        elif got_topic == 4:
            if not ProductTopic.objects.filter(id=topic_id).exists():
                return Response({"error":"midlevel with this id is not found"},status=status.HTTP_400_BAD_REQUEST)


        ser_data=CreateFieldSerializer(data=request.data)
        if ser_data.is_valid():
            created=ser_data.save()
            return Response({"message":"created","data":GetFieldSerializer(instance=created).data},status=status.HTTP_200_OK)
        else:
            return Response({"error":ser_data.errors},status=status.HTTP_400_BAD_REQUEST)

class GetMidlevelTopic(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        filter_kwargs={}
        if(request.data.get("toplevel_topic") is not None) and( request.data["toplevel_topic"] is not ""):
            filter_kwargs["toplevel_topic"] = request.data["toplevel_topic"]
        if(request.data.get("is_product") is not None) and( request.data["is_product"] is not ""):
            filter_kwargs["is_product"] = request.data["is_product"]
        if MidlevelTopic.objects.filter(**filter_kwargs).exists():
            ser_data=MidlevelTopicSerializer(MidlevelTopic.objects.filter(**filter_kwargs),many=True)
            return Response({"data":ser_data.data},status=status.HTTP_200_OK)
        else:
            return Response({"error":"there is not any midlevel topic"},status=status.HTTP_204_NO_CONTENT)


# class GetMidlevelTopic(APIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request):
#         filter_kwargs={}
#         if(request.data.get("search_key") is not None) and( request.data["search_key"] is not ""):
#             filter_kwargs["name__icontains"] = request.data["search_key"]
#         if(request.data.get("choosen") is not None) and( request.data["choosen"] is not ""):
#             filter_kwargs["is_choosen__is"] = request.data["choosen"]
#         if(request.data.get("filter") is not None) and( request.data["filter"] is not ""):
#             filter_kwargs["is_filter__is"] = request.data["filter"]
#         if(request.data.get("product") is not None) and( request.data["product"] is not ""):
#             filter_kwargs["is_product__is"] = request.data["product"]
#         if MidlevelTopic.objects.filter(**filter_kwargs).exists():
#             ser_data=MidlevelTopicSerializer(MidlevelTopic.objects.filter(**filter_kwargs),many=True)
#             return Response({"data":ser_data.data},status=status.HTTP_200_OK)
#         else:
#             return Response({"error":"there is not any midlevel topic"},status=status.HTTP_200_OK)



class SingleToplevelTopic(APIView):
    def get(self,request):
        if (request.query_params.get("toplevel_topic") is not None) and (request.query_params["toplevel_topic"]):
            if ToplevelTopic.objects.filter(id=request.query_params["toplevel_topic"]).exists():
                ser_data=ToplevelTopicSerializer(instance=ToplevelTopic.objects.get(id=request.query_params["toplevel_topic"]))
                return Response({"data":ser_data.data},status=status.HTTP_200_OK)
            else:
                return Response({"error":"there is not any toplevel topiv eit this id"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"please send toplevel_topic"},status=status.HTTP_400_BAD_REQUEST)



class SingleMidlevelTopic(APIView):
    def get(self,request):
        if (request.query_params.get("midlevel_topic") is not None) and (request.query_params["midlevel_topic"]):
            if MidlevelTopic.objects.filter(id=request.query_params["midlevel_topic"]).exists():
                ser_data=MidlevelTopicSerializer(instance=MidlevelTopic.objects.get(id=request.query_params["midlevel_topic"]))
                return Response({"data":ser_data.data},status=status.HTTP_200_OK)
            else:
                return Response({"error":"there is not any midlevel topic eit this id"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"please send midlevel_topic"},status=status.HTTP_400_BAD_REQUEST)

    


class SingleLowlevelTopic(APIView):
    def get(self,request):
        if (request.query_params.get("lowlevel_topic") is not None) and (request.query_params["lowlevel_topic"]):
            if LowlevelTopic.objects.filter(id=request.query_params["lowlevel_topic"]).exists():
                ser_data=LowlevelTopicSerializer(instance=LowlevelTopic.objects.get(id=request.query_params["lowlevel_topic"]))
                return Response({"data":ser_data.data},status=status.HTTP_200_OK)
            else:
                return Response({"error":"there is not any lowlevel topic eit this id"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"please send lowlevel_topic"},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        pass


class SingleProductTopic(APIView):
    def get(self,request):
        if (request.query_params.get("product_topic") is not None) and (request.query_params["product_topic"]):
            if ProductTopic.objects.filter(id=request.query_params["product_topic"]).exists():
                ser_data=ProductTopicSerializer(instance=ProductTopic.objects.get(id=request.query_params["product_topic"]))
                return Response({"data":ser_data.data},status=status.HTTP_200_OK)
            else:
                return Response({"error":"there is not any product topic eit this id"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"please send product_topic"},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        pass

class AllProductView(APIView):

    def post(self,request):
        if request.data.get("low_level_topic") is None or request.data["low_level_topic"]=="":
            return Response({"error":"please send low_level_topic"},status=status.HTTP_400_BAD_REQUEST)
        low_levle= request.data["low_level_topic"]
        products=Product.objects.filter(product_topic__lowlevel_topic=low_levle)
        