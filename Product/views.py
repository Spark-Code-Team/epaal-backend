from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import All_ToplevelSerializer, ConfirmedProductSerialiser, CreateProductInstanceSerialiser, CreateProductPictureSerialiser, CreateProductSerialiser, NotConfirmedProductSerialiser, ProductSerialiser, SingleProductserializer,ToplevelTopicSerializer,MidlevelTopicSerializer,ProductTopicSerializer,LowlevelTopicSerializer,CreateFieldSerializer,GetFieldSerializer,Product
from .models import FieldValue, MidlevelTopic, ProductDynamicField, ProductInstance, ProductStaticField, ProductTopic, StaticField, ToplevelTopic , LowlevelTopic
from rest_framework.parsers import MultiPartParser,FormParser
from django.contrib.contenttypes.models import ContentType
from Admin.models import Shop
from django.db import IntegrityError, transaction
import json
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
        products=Product.objects.filter()
        return Response(ProductSerialiser(instance=products,many=True).data,status=status.HTTP_200_OK)
    
class SingleProductView(APIView):

    def post(self,request):
        product_id=request.data.get("product_id")
        if not product_id:
            return Response({"error":"send product_id"},status=status.HTTP_400_BAD_REQUEST)
        if Product.objects.filter(id=product_id).exists():
            return Response({"data":SingleProductserializer(instance=Product.objects.get(id=product_id),context={"request":request}).data},status=status.HTTP_200_OK) 
        else:
            return Response({"error":"product with this  product_id is not found"},status=status.HTTP_400_BAD_REQUEST)


class CreateProductView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes=(MultiPartParser,FormParser)

    def post(self,request):
        if request.user.role.name != "shop_admin":
            return Response({"error":"you can't do this"},status=status.HTTP_400_BAD_REQUEST)
        
        product_topic_id=request.data.get("product_topic_id")
        product_name=request.data.get("name")
        product_data = request.data.copy()
        product_data["creator_id"] = request.user.id
        if not product_name:
            return Response({"error":"please send name"},status=status.HTTP_400_BAD_REQUEST)
        if not product_topic_id :
            return Response({"error":"please send product_topic_id"},status=status.HTTP_400_BAD_REQUEST)
        if Shop.objects.filter(shop_admin=request.user.id).exists() is False:
            return Response({"error":"you dont have shop"},status=status.HTTP_400_BAD_REQUEST)
        shop_id=Shop.objects.get(shop_admin=request.user.id).id
        product_data["shop"]=shop_id
        if ProductTopic.objects.filter(id=product_topic_id).exists():
            product_topic=ProductTopic.objects.get(id=product_topic_id)
            product_data["product_topic"]=product_topic.id
        else:
            raise ValueError("product topic not found")
        try:
        
            with transaction.atomic():
                product_ser_data=CreateProductSerialiser(data=product_data)
                if product_ser_data.is_valid():
                    product=product_ser_data.save() 
                else:
                    raise ValueError(product_ser_data.errors)

                ## handle product
                if request.data.get("static_fields"):
                    static_fields=json.loads(request.data["static_fields"])["static_fields"]
                    for send_static_field in static_fields:      
                        if send_static_field.get("field_id"):
                            field_id=send_static_field["field_id"]
                            if not StaticField.objects.filter(id=field_id).exists():
                                raise ValueError("static field not found")
                            static_field=StaticField.objects.get(id=field_id)
                            if static_field.is_choosable is False:
                                if send_static_field.get("field_value") is None:
                                    raise ValueError(f"send field_value of {static_field.name}")
                                else:
                                    ProductStaticField.objects.create(
                                        product=product,
                                        field=static_field,
                                        field_value=None,
                                        value=send_static_field["field_value"]
                                    )
                            else:
                                if send_static_field.get("field_value_id") is None:
                                    raise ValueError(f"send field_value_id of {static_field.name}")
                                else:
                                    if FieldValue.objects.filter(id=send_static_field.get("field_value_id")).exists():
                                        #! handle that product topic and field be same
                                        field_value=FieldValue.objects.get(id=send_static_field.get("field_value_id"))
                                        if field_value.static_field.id == static_field.id:
                                            ProductStaticField.objects.create(
                                                product=product,
                                                field=static_field,
                                                field_value=field_value,
                                                value=None
                                            )
                                        else:
                                            raise ValueError(f" in static fields product topic and field are not same")
                                        
                                    else:
                                        raise ValueError(f'there is not any field value with id { send_static_field["field_value_id"] }')
                print("!111111111111111111111111111111111111111111")
                ## handle instance 
                if request.data.get("instance") is None:
                    raise ValueError("send at least one instance")
                instances=json.loads(request.data["instance"])["instance"]
                for instance in instances:   
                    discount=0
                    if instance.get("capacity") is None:
                        raise ValueError('send capacity for all object')
                    if instance.get("price") is None:
                        raise ValueError('send price for all object')
                    if instance.get("discount") is not None:
                        if ((instance.get("discount")>100) or( instance.get("discount")<0)):
                            raise ValueError("discount muset be in range 0 and 100")
                        discount=instance.get("discount")
                    instance_data={
                        "product":product.id,
                        "capacity":instance.get("capacity"),
                        "price":instance.get("capacity"),
                        "discount":discount
                            }
                    instance_ser_date=CreateProductInstanceSerialiser(data=instance_data)
                    if instance_ser_date.is_valid():
                        created_instance=instance_ser_date.save()
                    else:   
                        raise ValueError(instance_ser_date.errors)  

                    print(instance)
                    if instance.get("field_id"):
                        field_id=instance["field_id"]
                        if not StaticField.objects.filter(id=field_id).exists():
                            raise ValueError("static field not found")
                        static_field=StaticField.objects.get(id=field_id)
                        if static_field.is_choosable is False:
                            if instance.get("field_value") is None:
                                raise ValueError(f"send field_value of {static_field.name}")
                            else:
                                ProductDynamicField.objects.create(
                                    product_instance=created_instance,
                                    field=static_field,
                                    field_value=None,
                                    value=instance["field_value"]
                                )
                        else:
                            if instance.get("field_value_id") is None:
                                raise ValueError(f"send field_value_id of {static_field.name}")
                            else:
                                if FieldValue.objects.filter(id=instance.get("field_value_id")).exists():
                                    #! handle that product topic and field be same
                                    field_value=FieldValue.objects.get(id=instance.get("field_value_id"))
                                    if field_value.static_field.id == static_field.id:
                                        ProductDynamicField.objects.create(
                                            product_instance=created_instance,
                                            field=static_field,
                                            field_value=field_value,
                                            value=None
                                        )
                                    else:
                                        raise ValueError(f"in instance product topic and field are not same")
                                    
                                else:
                                    raise ValueError(f'there is not any field value with id { instance["field_value_id"] }')
                ## handle pictures
                data=[]
                index = 0
                while f"picture[{index}]" in request.data:
                    file_obj = request.data.get(f"picture[{index}]")
                    if file_obj:
                        data.append({
                            "product":product.id,
                            "product_pic":file_obj
                        })
                    index += 1
                if len(data) != 0:
                    picture_ser_data=CreateProductPictureSerialiser(data=data,many=True)
                    if picture_ser_data.is_valid():
                        picture_ser_data.save()
                    else:
                        raise ValueError(picture_ser_data.errors)

                
                return Response({"message":"product is created"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        

class ShopProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        if request.user.role.name != "shop_admin":
            return Response({"error":"you can't do this"},status=status.HTTP_400_BAD_REQUEST)
        
        if Shop.objects.filter(shop_admin=request.user.id).exists() is False:
            return Response({"error":"you dont have shop"},status=status.HTTP_400_BAD_REQUEST) 
        shop_id=Shop.objects.get(shop_admin=request.user.id).id
        
        if request.GET.get("is_comfirmed") is None:
            return Response({"error":"please send is_comfirmed  "},status=status.HTTP_400_BAD_REQUEST) 
        
        if request.GET["is_comfirmed"] not in ["false","true",False,True]:
            return Response({"error":"is_comfirmed   should be True or False"},status=status.HTTP_400_BAD_REQUEST)
        
        if request.GET["is_comfirmed"] == True or request.GET["is_comfirmed"]=="true":
            products=Product.objects.filter(shop=shop_id,is_confirm=True)
            if len(products) == 0:
                return Response({"error":"there is not any product"},status=status.HTTP_204_NO_CONTENT)
            return Response (ConfirmedProductSerialiser(instance=products,many=True,context = {"request": request}).data,status=status.HTTP_200_OK)
        elif request.GET["is_comfirmed"] == False or request.GET["is_comfirmed"]=="false":
            products=Product.objects.filter(shop=shop_id,is_confirm=False)
            if len(products) == 0:
                return Response({"error":"there is not any product"},status=status.HTTP_204_NO_CONTENT)
            return Response (NotConfirmedProductSerialiser(instance=products,many=True,context = {"request": request}).data,status=status.HTTP_200_OK)

