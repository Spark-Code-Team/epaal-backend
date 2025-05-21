from django.db import models
from User.models import CustomUser
from django.template.defaultfilters import filesizeformat
from django.core.validators import ValidationError, FileExtensionValidator
from django.core.files.base import ContentFile
from EvaamBack import settings
from django.core.files.storage import default_storage

# Create your models here.
def validate_image_size(image):
    filesize = image.size
    if filesize > int(settings.MAX_UPLOAD_IMAGE_SIZE):
        raise ValidationError('Max image size should be '.format((filesizeformat(settings.MAX_UPLOAD_IMAGE_SIZE))))
    
def shop_image_directory_path(instance, filename):
    return 'shop/{0}/logoes/{1}'.format(str(instance.id), filename) 

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
    VALID_AVATAR_EXTENSION = ['png', 'jpg', 'jpeg']   

    shop_name = models.CharField(max_length=100,null=False,blank=False)
    shop_phone=models.CharField(max_length=11,null=False,blank=False)
    address=models.CharField(max_length=500,null=False,blank=False)
    bio=models.CharField(max_length=500)
    shop_admin=models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name="shop_admin")
    shop_logo=models.ImageField(upload_to=shop_image_directory_path,
                               validators=[FileExtensionValidator(VALID_AVATAR_EXTENSION), validate_image_size],
                               blank=True, null=True, max_length=1000)
    
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'shop'
        verbose_name_plural = 'shops'
        db_table = 'shop'

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_image = self.shop_logo
            self.shop_logo = None
            super(Shop, self).save(*args, **kwargs)
            if saved_image:
                path=shop_image_directory_path(self,saved_image)
                default_storage.save(path, ContentFile(saved_image.read()))
                self.shop_logo = path
            else:
                self.shop_logo = None
            self.save()
        else:
            super(Shop, self).save(*args, **kwargs) 

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