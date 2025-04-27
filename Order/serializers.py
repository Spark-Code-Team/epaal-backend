from rest_framework import serializers

from User.serializers import UserWalletSerialiser,AddressSerializer

from .models import Order,BoughtOrder
from Product.serializers import AllProductInstanceSerializer
class BoughtOrderSeializer(serializers.ModelSerializer):
    product_intance=AllProductInstanceSerializer()
    class Meta:
        model=BoughtOrder
        fields=("id","product_intance","product_discount","all_discount","product_cost","paid_cost")

class OrderSerializer(serializers.ModelSerializer):
    bought_product_instances=serializers.SerializerMethodField()
    address=AddressSerializer()
    transaction=UserWalletSerialiser()

    class Meta:
        model=Order
        fields=("id","address","all_price","delivery_price","status","transaction","num_of_product","is_paid","created_at","bought_product_instances")

    def get_bought_product_instances(self,obj):
        bought_product=BoughtOrder.objects.filter(order=obj.id)
        return BoughtOrderSeializer(instance=bought_product,many=True).data