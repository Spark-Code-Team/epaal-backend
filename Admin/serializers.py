from rest_framework import serializers
from .models import Shop,Provider,ProviderBranch
from Product.models import MidlevelTopic,MidlevelTopicProviderBranch

class ShopSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shop
        fields = ("id",'shop_name','shop_phone','address','bio','shop_admin','shop_topic',)

        extra_kwargs={
            'bio':{"required":False}
        }

    def update(self, instance, validated_data):

        instance.shop_name = validated_data.get('shop_name', instance.shop_name)
        instance.shop_phone = validated_data.get('shop_phone', instance.shop_phone)
        instance.address = validated_data.get('address', instance.address)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance



class AllShopSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shop
        fields = ('id','shop_name',)


class ProviderBranchSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProviderBranch
        fields = ('id','name')
class ProviderBranchWithProviderSerializer(serializers.ModelSerializer):
    provider=ProviderBranchSerializer(read_only=True)
    class Meta:
        model = ProviderBranch
        fields = ('id','name',"provider")
        
class MidlevelTopicProviderBranchSerializer(serializers.ModelSerializer):
    provider_branch=ProviderBranchSerializer()
    
    class Meta:
        model = MidlevelTopicProviderBranch
        fields = ('id','provider_branch')



class SingleShopSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shop
        fields = "__all__"

        
