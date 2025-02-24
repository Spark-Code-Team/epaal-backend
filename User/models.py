from django.db import models
from Role.models import Role
from django.contrib.auth.models import (
    PermissionsMixin,
    AbstractBaseUser,
    BaseUserManager,
)
from User.managers import UserManager

# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    first_name=models.CharField(max_length=50,null=True,blank=True)
    last_name=models.CharField(max_length=50,null=True,blank=True)
    national_code=models.CharField( max_length=10,unique=True,null=True,blank=True)
    phone_number=models.CharField(max_length=11,unique=True,null=False,blank=False)
    second_phone_number=models.CharField(max_length=11,null=True,blank=True)
    is_man=models.BooleanField(null=True,blank=True)
    birthday_date=models.CharField(max_length=10,null=True,blank=True)
    shamsi_birthday_date=models.CharField(max_length=10,null=True,blank=True)
    referrer_code = models.CharField(max_length=90, blank=True, null=True)
    inviter = models.ForeignKey('self', on_delete=models.CASCADE, related_name='invited', blank=True, null=True)
    role = models.ForeignKey(to=Role, on_delete=models.CASCADE, null=True, blank=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    has_two_factor=models.BooleanField(default=False)
    confirmed_data=models.BooleanField(default=False)
    confirmed_address=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ["role"]

    class Meta:
        ordering = ['created_at']
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'user'


    @property
    def is_staff(self):
        return self.is_admin


class Address(models.Model):
    address=models.CharField(max_length=1000)
    postal_code=models.CharField(max_length=10)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="user_address")

    class Meta:
        verbose_name = 'address'
        verbose_name_plural = 'addresses'
        db_table = 'address'


class OTP(models.Model):
    phone_number=models.CharField(max_length=11)
    otp_code=models.CharField(max_length=8)
    otp_expire=models.DateTimeField(null=False,blank=False)
    max_try=models.IntegerField(default=3,max_length=2)
    otp_for=models.CharField(max_length=50,default="login")
    class Meta:
        verbose_name = 'otp'
        verbose_name_plural = 'otps'
        db_table = 'otp'

class JibitToken(models.Model):
    access_token=models.CharField(max_length=400)
    refresh_token=models.CharField(max_length=400)
    created_at=models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'jibit_token'
        verbose_name_plural = 'jibit_tokens'
        db_table = 'jibit_token'

class TempAddress(models.Model):
    postal_code=models.CharField(max_length=10)
    address=models.CharField(max_length=1000)
