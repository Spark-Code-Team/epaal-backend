from django.db import models
from User.models import CustomUser
# Create your models here.

class Shop(models.Model):
    shop_name = models.CharField(max_length=100,null=False,blank=False)
    shop_phone=models.CharField(max_length=11,null=False,blank=False)
    address=models.CharField(max_length=500,null=False,blank=False)
    bio=models.CharField(max_length=500)
    shop_admin=models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name="shop_admin")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'shop'
        verbose_name_plural = 'shops'
        db_table = 'shop'

    def __str__(self):
        return self.name