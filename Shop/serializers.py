from rest_framework import serializers

from Shop.models import ShopRequest

class ShopRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopRequest
        fields = '__all__'
class CreateShopRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopRequest
        fields = ('shop_name', 'first_name', 'last_name', 'phone_number', 'site_url')
