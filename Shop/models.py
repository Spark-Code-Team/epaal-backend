from django.db import models

# Create your models here.

class ShopRequest(models.Model):
    shop_name = models.CharField(max_length=255, verbose_name="Shop Name")
    first_name = models.CharField(max_length=255, verbose_name="Name")
    last_name = models.CharField(max_length=255, verbose_name="Last Name")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")
    site_url = models.URLField(max_length=255, verbose_name="Site URL")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    is_confirmed = models.BooleanField(default=False, verbose_name="Is Confirmed")

    class Meta:
        verbose_name = "Shop Request"
        verbose_name_plural = "Shop Requests"
