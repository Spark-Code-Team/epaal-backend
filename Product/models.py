from django.db import models
from Admin.models import Shop
from EvaamBack import settings
from django.template.defaultfilters import filesizeformat
from django.core.validators import ValidationError, FileExtensionValidator
from User.models import CustomUser
# Create your models here.



def validate_image_size(image):
    filesize = image.size
    if filesize > int(settings.MAX_UPLOAD_IMAGE_SIZE):
        raise ValidationError('Max image size should be '.format((filesizeformat(settings.MAX_UPLOAD_IMAGE_SIZE))))
    
def product_image_directory_path(instance, filename):
    return 'Media/product/{0}/pictures/{1}'.format(str(instance.id), filename) 

class ProductTopic(models.Model):
    name=models.CharField(max_length=100)

    class Meta:
        verbose_name = 'product_topic'
        verbose_name_plural = 'product_topics'
        db_table = 'product_topic'

class ProductSpecification(models.Model):
    key=models.CharField(max_length=100)
    value=models.CharField(max_length=100)

    class Meta:
        verbose_name = 'product_specification'
        verbose_name_plural = 'Product_specifications'
        db_table = 'product_specification'

class ProductPicture(models.Model):
    VALID_AVATAR_EXTENSION = ['png', 'jpg', 'jpeg']   
    product_pic= models.ImageField(upload_to=product_image_directory_path,
                               validators=[FileExtensionValidator(VALID_AVATAR_EXTENSION), validate_image_size],
                               blank=True, null=True, max_length=1000)
    class Meta:
        verbose_name = 'product_picture'
        verbose_name_plural = 'product_pictures'
        db_table = 'product_picture'




class Product(models.Model):
    name = models.CharField(max_length=100)
    price=models.CharField(max_length=20)
    discount=models.IntegerField(max_length=3)
    shop=models.ForeignKey(Shop,on_delete=models.CASCADE, related_name="subjects_of_titles")
    product_topic=models.ForeignKey(ProductTopic,on_delete=models.CASCADE, related_name="subject_topic")
    is_in_event=models.BooleanField(default=False)
    is_new=models.BooleanField(default=False)
    num_of_seen=models.IntegerField(default=0)
    is_confirm=models.BooleanField(default=False)
    detail=models.CharField(max_length=500)
    rate=models.IntegerField(default=0)
    num_of_rates=models.IntegerField(default=0)
    creator_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="creator_id")
    product_specification=models.ManyToManyField(ProductSpecification,null=True,blank=True)
    product_picture=models.ManyToManyField(ProductPicture,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        db_table = 'product'

    
class ProductColor(models.Model):
    name=models.CharField(max_length=100)

    class Meta:
        verbose_name = 'product_color'
        verbose_name_plural = 'product_colors'
        db_table = 'product_color'

class AvailableProduct(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="availbal_product")
    color=models.ForeignKey(ProductColor,on_delete=models.CASCADE,related_name="availbal_product_color")
