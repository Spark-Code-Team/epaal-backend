from django.db import models
from User.models import CustomUser
# Create your models here.

class Shop(models.Model):
    shop_name = models.CharField(max_length=100)
    shop_phone=models.CharField(max_length=11)
    address=models.CharField(max_length=500)
    bio=models.CharField(max_length=500)
    shop_admin=models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name="shop_admin")

    class Meta:
        verbose_name = 'shop'
        verbose_name_plural = 'shops'
        db_table = 'shop'

    def __str__(self):
        return self.name