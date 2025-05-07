from django.db import models

# Create your models here.

class ShopRequest(models.Model):
    shop_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    site_url = models.URLField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Shop Request"
        verbose_name_plural = "Shop Requests"
