from rest_framework import serializers

from Admin.models import Shop
from .models import ProductDynamicField, ProductPicture, ProductStaticField, ToplevelTopic,MidlevelTopic,ProductTopic,Product,LowlevelTopic,StaticField,ProductInstance,FieldValue


from Product.serializers import AllProductInstanceSerializer

class ToplevelTopicSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ToplevelTopic
        fields = ('id','name','picture',)

        
class MidlevelTopicSerializer(serializers.ModelSerializer):
    toplevel_topic=ToplevelTopicSerializer
    class Meta:
        model = MidlevelTopic
        fields = ('id','name','toplevel_topic','picture','is_product',)
        extra_kwargs={
            'is_product':{"default":True}
        }
        
class LowlevelTopicSerializer(serializers.ModelSerializer):
    midlevel_topic=MidlevelTopicSerializer
    class Meta:
        model = LowlevelTopic
        fields = ('id','name','midlevel_topic','picture',)
        


class ProductTopicSerializer(serializers.ModelSerializer):
    lowlevel_topic=LowlevelTopicSerializer
    class Meta:
        model = ProductTopic
        fields = ('id','name','lowlevel_topic','picture',)


class All_TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTopic
        fields = ('id','name','picture',)

        
class All_LowlevelSerializer(serializers.ModelSerializer):
    product_topic=serializers.SerializerMethodField()
    class Meta:
        model = LowlevelTopic
        fields = ('id','name','product_topic','picture',)

    def get_product_topic(self,obj):
        if not ProductTopic.objects.filter(lowlevel_topic=obj.id).exists():
            return None
        ser_data=All_TopicSerializer(instance=ProductTopic.objects.filter(lowlevel_topic=obj.id),many=True)
        return ser_data.data 
    
class All_MidlevelSerializer(serializers.ModelSerializer):
    lowlevel_topic=serializers.SerializerMethodField()
    class Meta:
        model = MidlevelTopic
        fields = ('id','name','lowlevel_topic','picture','is_product')

    def get_lowlevel_topic(self,obj):
        if not LowlevelTopic.objects.filter(midlevel_topic=obj.id).exists():
            return None
        ser_data=All_LowlevelSerializer(instance=LowlevelTopic.objects.filter(midlevel_topic=obj.id),many=True)
        return ser_data.data 


class All_ToplevelSerializer(serializers.ModelSerializer):
    midlevel_topic=serializers.SerializerMethodField()
    class Meta:
        model = ToplevelTopic
        fields = ('id','name','midlevel_topic','picture',)

    def get_midlevel_topic(self,obj):
        if not MidlevelTopic.objects.filter(toplevel_topic=obj.id).exists():
            return None
        ser_data=All_MidlevelSerializer(instance=MidlevelTopic.objects.filter(toplevel_topic=obj.id),many=True)
        return ser_data.data


class CreateFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticField
        fields = ("id","name",'is_filter','is_choosable','topic_level','object_id')
class FieldValueSerializer(serializers.ModelSerializer):
    class Meta:
        model=FieldValue
        fields=("id","value")  
        
class GetFieldForCreateProductSerializer(serializers.ModelSerializer):
    options=serializers.SerializerMethodField()
    class Meta:
        model = StaticField
        fields = ("id","name",'is_filter','is_choosable',"options",)
    
    def get_options(self,obj):
        if obj.is_choosable:
            if FieldValue.objects.filter(static_field=obj.id).exists():
                return FieldValueSerializer(instance=FieldValue.objects.filter(static_field=obj.id),many=True).data
            else:
                return []
        else:
            None



class GetFieldSerializer(serializers.ModelSerializer):
    object=serializers.SerializerMethodField()
    class Meta:
        model = StaticField
        fields = ("id","name",'is_filter','is_choosable','object','topic_level','object_id')

    def get_object(self,obj):
        if obj.topic_level==2:
            if MidlevelTopic.objects.filter(id=obj.object_id).exists():
                return MidlevelTopicSerializer(instance=MidlevelTopic.objects.get(id=obj.object_id)).data
            else:
                return None
        elif obj.topic_level==3:
            if LowlevelTopic.objects.filter(id=obj.object_id).exists():
                return LowlevelTopicSerializer(instance=LowlevelTopic.objects.get(id=obj.object_id)).data
            else:
                return None  
        elif obj.topic_level==4:
            if ProductTopic.objects.filter(id=obj.object_id).exists():
                return ProductTopicSerializer(instance=ProductTopic.objects.get(id=obj.object_id)).data
            else:
                return None
        else:
            return None
            
class ProductInstanceSerialiser(serializers.ModelSerializer):

    class Meta:
        model=ProductInstance
        fields=("__all__")

class ProductInstanceForProductSerialiser(serializers.ModelSerializer):

    class Meta:
        model=ProductInstance
        fields=("id","capacity","price","discount")
class ShopSerialiser(serializers.ModelSerializer):

    class Meta:
        model=Shop
        fields=("__all__")
class ShopForUserPanelSerialiser(serializers.ModelSerializer):

    class Meta:
        model=Shop
        fields=("id","shop_name")

class LowlevelTopicSerialiser(serializers.ModelSerializer):
    class Meta:
        model=LowlevelTopic
        fields=("__all__")

class ProductTopicSerialiser(serializers.ModelSerializer):
    lowlevel_topic=LowlevelTopicSerialiser()
    class Meta:
        model=ProductTopic
        fields=("__all__")

 
class ProductSerialiser(serializers.ModelSerializer):
    product_instances=serializers.SerializerMethodField()
    field=serializers.SerializerMethodField()
    fake_picture=serializers.SerializerMethodField()
    shop=ShopSerialiser()
    product_topic=ProductTopicSerialiser()
    class Meta:
        model=Product
        fields=("id","name","shop","product_topic","detail","rate","num_of_rates","created_at","product_instances","field","fake_picture","product_topic")
        
    def get_product_instances(self,obj):
        products=ProductInstance.objects.filter(product=obj.id)
        return ProductInstanceForProductSerialiser(instance=products,many=True).data
     
    def get_field(self,obj):
        return {"field1":"value1","field2":"value2","field3":"value3","field4":"value4","field5":"value5"}
    
    def get_fake_picture(self,obj):
        if obj.id==1:
            return "https://dkstatics-public.digikala.com/digikala-products/c23b49b0be1c4ae5b2a3d7a3281d2f1731065243_1726037574.jpg?x-oss-process=image/resize,m_lfit,h_800,w_800/format,webp/quality,q_90"
        elif obj.id==2:
            return "https://digimarketplus.ir/wp-content/uploads/2021/09/%D8%AE%D8%B1%DB%8C%D8%AF-%DB%8C%D8%AE%DA%86%D8%A7%D9%84-%D8%A7%D8%B3%D9%86%D9%88%D8%A7.jpg"
        elif obj.id==3:
            return "https://www.sanggallery.com/upload/product/1722332861-Shiseido-Clarelifying-Cleansing-Foam.jpg"
        elif obj.id==4:
            return "https://www.motormarkett.com/wp-content/uploads/scoopy1.png"
        elif obj.id==5:
            return "https://image.torob.com/base/images/J0/vJ/J0vJxuUdz-CKf_ez.jpg_/560x560.webp"
        elif obj.id==6:
            return "https://www.toolsap.com/wp-content/uploads/2018/05/gcai150r.jpg"
        elif obj.id==7:
            return "https://shob360.com/wp-content/uploads/2021/08/1-3.jpg"
        else:
            return None
class NormalProductSerialiser(serializers.ModelSerializer):
    fake_picture=serializers.SerializerMethodField()
    field=serializers.SerializerMethodField()

    class Meta:
        model=Product
        fields=("__all__")
     
    def get_field(self,obj):
        return {"field1":"value1","field2":"value2","field3":"value3","field4":"value4","field5":"value5"}
    def get_fake_picture(self,obj):
        if obj.id==1:
            return "https://dkstatics-public.digikala.com/digikala-products/c23b49b0be1c4ae5b2a3d7a3281d2f1731065243_1726037574.jpg?x-oss-process=image/resize,m_lfit,h_800,w_800/format,webp/quality,q_90"
        elif obj.id==2:
            return "https://digimarketplus.ir/wp-content/uploads/2021/09/%D8%AE%D8%B1%DB%8C%D8%AF-%DB%8C%D8%AE%DA%86%D8%A7%D9%84-%D8%A7%D8%B3%D9%86%D9%88%D8%A7.jpg"
        elif obj.id==3:
            return "https://www.sanggallery.com/upload/product/1722332861-Shiseido-Clarelifying-Cleansing-Foam.jpg"
        elif obj.id==4:
            return "https://www.motormarkett.com/wp-content/uploads/scoopy1.png"
        elif obj.id==5:
            return "https://image.torob.com/base/images/J0/vJ/J0vJxuUdz-CKf_ez.jpg_/560x560.webp"
        elif obj.id==6:
            return "https://www.toolsap.com/wp-content/uploads/2018/05/gcai150r.jpg"
        elif obj.id==7:
            return "https://shob360.com/wp-content/uploads/2021/08/1-3.jpg"
        else:
            return None
class ProductInstanceSerialiser(serializers.ModelSerializer):
    product=AllProductInstanceSerializer()
    class Meta:
        model=ProductInstance
        fields=("product")




#############################################################

class CreateProductSerialiser(serializers.ModelSerializer):


    class Meta:
        model=Product
        fields=("name","shop","product_topic","detail","creator_id")

class CreateProductPictureSerialiser(serializers.ModelSerializer):
    class Meta:
        model=ProductPicture
        fields=("id","product","product_pic")
class CreateProductInstanceSerialiser(serializers.ModelSerializer):
    class Meta:
        model=ProductInstance
        fields=("__all__")

class ProductPictureSerialiser(serializers.ModelSerializer):
    class Meta:
        model=ProductPicture
        fields=("id","product_pic")

class ConfirmedProductSerialiser(serializers.ModelSerializer):
    pircture=serializers.SerializerMethodField()
    class Meta:
        model=Product
        fields=("id","name","created_at","pircture")

    def get_pircture(self,obj):
        if ProductPicture.objects.filter(product=obj.id).exists():
            return ProductPictureSerialiser(instance=ProductPicture.objects.filter(product=obj.id).first(),context = {"request": self.context.get("request")}).data
        else:
            return None
        
class NotConfirmedProductSerialiser(serializers.ModelSerializer):
    pircture=serializers.SerializerMethodField()
    status=serializers.SerializerMethodField()
    class Meta:
        model=Product
        fields=("id","name","created_at","pircture","report_message","status")

    def get_pircture(self,obj):
        if ProductPicture.objects.filter(product=obj.id).exists():
            return ProductPictureSerialiser(instance=ProductPicture.objects.filter(product=obj.id).first(),context = {"request": self.context.get("request")}).data
        else:
            return None
        
    def get_status(self,obj):
        if obj.report_message:
            return "not_confirmed"
        else:
            return "unseen"



class ProductDynamicFieldSerialier(serializers.ModelSerializer):

    class Meta:
        model=ProductDynamicField
        fields=("field","field_value","value")
        depth=1

class SingleProductINstanceserializer(serializers.ModelSerializer):
    dynamic_fields=serializers.SerializerMethodField()
    class Meta:
        model=ProductInstance
        fields=("id","price","discount","capacity","dynamic_fields")

    def get_dynamic_fields(self,obj):
        if ProductDynamicField.objects.filter(product_instance=obj.id).exists() is False:
            return None
        return ProductDynamicFieldSerialier(instance=ProductDynamicField.objects.filter(product_instance=obj.id),many=True).data

class ProductStaticFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model=ProductStaticField
        fields=("field","field_value","value")
        depth=1


class SingleProductTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model=ProductTopic
        fields=("id","name","picture")

class SingleLowlevelTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model=LowlevelTopic
        fields=("id","name","picture")

class SingleMidlevelTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model=MidlevelTopic
        fields=("id","name","picture")

class SingleToplevelTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model=ToplevelTopic
        fields=("id","name","picture")

class SingleProductserializer(serializers.ModelSerializer):
    static_fileds=serializers.SerializerMethodField()
    instances=serializers.SerializerMethodField()
    shop=ShopForUserPanelSerialiser()
    iamges=serializers.SerializerMethodField()
    product_topic=SingleProductTopicSerializer()
    lowlevel_topic=serializers.SerializerMethodField()
    midlevel_topic=serializers.SerializerMethodField()
    toplevel_topic=serializers.SerializerMethodField()

    

    class Meta:
        model=Product
        fields=("id","name","shop","detail","rate","static_fileds","instances","iamges","product_topic","lowlevel_topic","midlevel_topic","toplevel_topic")

    def get_static_fileds(self,obj):
        if ProductStaticField.objects.filter(product=obj.id).exists() is False:
            return None
        else:
            return ProductStaticFieldSerializer(ProductStaticField.objects.filter(product=obj.id),many=True).data


    def get_instances(self,obj):
        if ProductInstance.objects.filter(product=obj.id).exists() is False:
            return None
        else:
            return SingleProductINstanceserializer(ProductInstance.objects.filter(product=obj.id),many=True).data
        
    def get_iamges(self,obj):
        if ProductPicture.objects.filter(product=obj.id).exists() is False:
            return None
        return ProductPictureSerialiser(ProductPicture.objects.filter(product=obj.id),many=True,context={"request":self.context.get("request")}).data

    def get_lowlevel_topic(self,obj):
        return SingleLowlevelTopicSerializer(obj.product_topic.lowlevel_topic).data
    
    def get_midlevel_topic(self,obj):
        return SingleMidlevelTopicSerializer(obj.product_topic.lowlevel_topic.midlevel_topic).data
    
    def get_toplevel_topic(self,obj):
        return SingleToplevelTopicSerializer(obj.product_topic.lowlevel_topic.midlevel_topic.toplevel_topic).data
    


class AllProductInstanceSerializer(serializers.ModelSerializer):
    product_id=serializers.SerializerMethodField()
    product_image=serializers.SerializerMethodField()
    product_name=serializers.SerializerMethodField()
    class Meta:
        model=ProductInstance
        fields=("id","product_id","product_image","product_name","price")

    def get_product_id(self,obj):
        return obj.product.id
    
    def get_product_image(self,obj):
        return ProductPictureSerialiser(ProductPicture.objects.filter(product=obj.product).first(),context={"request":self.context.get("request")}).data
    
    def get_product_name(self,obj):
        return obj.product.name

