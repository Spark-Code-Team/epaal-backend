from rest_framework import serializers
from .models import ToplevelTopic,MidlevelTopic,ProductTopic,Product




class ToplevelTopicSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ToplevelTopic
        fields = ('id','name',)

        
class MidlevelTopicSerializer(serializers.ModelSerializer):
    toplevel_topic=ToplevelTopicSerializer
    class Meta:
        model = MidlevelTopic
        fields = ('id','name','toplevel_topic',)
        


class ProductTopicSerializer(serializers.ModelSerializer):
    midlevel_topic=MidlevelTopicSerializer
    class Meta:
        model = ProductTopic
        fields = ('id','name','midlevel_topic',)


class All_TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTopic
        fields = ('id','name',)

        
class All_MidlevelSerializer(serializers.ModelSerializer):
    topic=serializers.SerializerMethodField()
    class Meta:
        model = MidlevelTopic
        fields = ('id','name','topic',)

    def get_topic(self,obj):
        if not ProductTopic.objects.filter(midlevel_topic=obj.id).exists():
            return None
        ser_data=All_TopicSerializer(instance=ProductTopic.objects.filter(midlevel_topic=obj.id),many=True)
        return ser_data.data 


class All_ToplevelSerializer(serializers.ModelSerializer):
    midlevel_topic=serializers.SerializerMethodField()
    class Meta:
        model = ToplevelTopic
        fields = ('id','name','midlevel_topic',)

    def get_midlevel_topic(self,obj):
        if not MidlevelTopic.objects.filter(toplevel_topic=obj.id).exists():
            return None
        ser_data=All_MidlevelSerializer(instance=MidlevelTopic.objects.filter(toplevel_topic=obj.id),many=True)
        return ser_data.data
