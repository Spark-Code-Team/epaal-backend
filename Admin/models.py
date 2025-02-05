from django.db import models
from User.models import CustomUser
# Create your models here.

class ShopTopic(models.Model):
    start_date = models.DateTimeField(null=False,blank=False)
    end_date = models.DateTimeField(null=False,blank=False)
    payment_date = models.DateTimeField(default=None)
    percent=models.FloatField(default=0.0)
    midlevel_topic=models.ForeignKey('Product.MidlevelTopic',on_delete=models.CASCADE,related_name="shop_midlevel_topic_topic")
    status=models.CharField(default="before_of_time",max_length=100)

    class Meta:
        verbose_name = 'shop_topic'
        verbose_name_plural = 'shop_topics'
        db_table = 'shop_topic'

class Shop(models.Model):
    shop_name = models.CharField(max_length=100,null=False,blank=False)
    shop_phone=models.CharField(max_length=11,null=False,blank=False)
    address=models.CharField(max_length=500,null=False,blank=False)
    bio=models.CharField(max_length=500)
    shop_admin=models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name="shop_admin")
    shop_topic=models.ManyToManyField(ShopTopic,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'shop'
        verbose_name_plural = 'shops'
        db_table = 'shop'

class Provider(models.Model):
    name=models.CharField(max_length=100,null=False,blank=False)

    class Meta:
        verbose_name = 'provider'
        verbose_name_plural = 'providers'
        db_table = 'provider'

class ProviderBranch(models.Model):
    name=models.CharField(max_length=100,null=False,blank=False)
    user_name=models.CharField(max_length=100,null=False,blank=False)
    password=models.CharField(max_length=100,null=False,blank=False)
    provider=models.ForeignKey(Provider,on_delete=models.CASCADE,related_name="provider_branch")
    api_url=models.CharField(max_length=500,null=False,blank=False)
    percent=models.FloatField(default=0.0)
    class Meta:
        verbose_name = 'provider_branch'
        verbose_name_plural = 'provider_branchs'
        db_table = 'provider_branch'