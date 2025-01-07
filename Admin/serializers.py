from rest_framework import serializers
from .models import Shop


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

        
class SingleShopSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shop
        fields = "__all__"

        
