from django.db import models

from Product.models import Product, ProductInstance
from User.models import CustomUser,Address
from Transaction.models import Tranaction
# Create your models here.
class Cart(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="user_id_cart")
    products=models.ManyToManyField(ProductInstance,related_name="product_id_cart",null=True,blank=True)

    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'
        db_table = 'cart'


class Order(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="user_id_order")
    products=models.ManyToManyField(Product,related_name="product_ids_order")
    address=models.ForeignKey(Address,on_delete=models.CASCADE,related_name="address_id_order")
    all_price=models.IntegerField(max_length=30)
    delivery_price=models.IntegerField(max_length=30)
    status=models.CharField(max_length=50)
    transaction=models.ForeignKey(Tranaction,on_delete=models.CASCADE,related_name="transaction_id_order")
    num_of_product=models.IntegerField(default=1)
    is_paid=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        db_table = 'order'

class BoughtOrder(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="user_id_bought_order")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_id_bought_order")
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_id_bought_order")
    product_discount=models.IntegerField(max_length=3)
    all_discount=models.IntegerField(max_length=3)
    product_cost=models.IntegerField(max_length=30)
    paid_cost=models.IntegerField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'bought_order'
        verbose_name_plural = 'bought_orders'
        db_table = 'bought_order'
