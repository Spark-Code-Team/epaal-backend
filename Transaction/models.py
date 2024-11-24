from django.db import models
from User.models import CustomUser
# Create your models here.

class Tranaction(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="user_transaction")
    value=models.IntegerField(max_length=20)
    status=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'transaction'
        verbose_name_plural = 'transactions'
        db_table = 'transaction'
