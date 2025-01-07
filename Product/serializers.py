from rest_framework import serializers
from .models import ToplevelTopic,MidlevelTopic,ProductTopic,Product,LowlevelTopic




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
