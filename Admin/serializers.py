from rest_framework import serializers
from .models import Shop


class ShopSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shop
        fields = ('shop_name','shop_phone','address','bio','shop_admin')

        extra_kwargs={
            'bio':{"required":False}
        }
