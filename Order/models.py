from django.db import models

from Product.models import Product, ProductInstance
from User.models import CustomUser,Address, UserCreditTransaction
from Transaction.models import Tranaction
# Create your models here.
class Cart(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="user_id_cart")

    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'
        db_table = 'cart'

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_id_cart_item")
    product_instance=models.ForeignKey(ProductInstance,on_delete=models.CASCADE,related_name="product_instance_id_cart_item")
    quantity=models.IntegerField(default=1)

    class Meta:
        verbose_name = 'cart_item'
        verbose_name_plural = 'cart_items'
        db_table = 'cart_item'
        

class Order(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="user_id_order")
    product_intances=models.ManyToManyField(ProductInstance,related_name="product_ids_order")
    address=models.ForeignKey(Address,on_delete=models.CASCADE,related_name="address_id_order")
    all_price=models.IntegerField(max_length=30)
    delivery_price=models.IntegerField(max_length=30)
    status=models.CharField(max_length=50)
    transaction=models.ForeignKey(UserCreditTransaction,on_delete=models.CASCADE,related_name="transaction_id_order")
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
    product_intance=models.ForeignKey(ProductInstance,on_delete=models.CASCADE,related_name="product_id_bought_order")
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
