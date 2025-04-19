from django.db import models
from Admin.models import Shop,ProviderBranch
from EvaamBack import settings
from django.template.defaultfilters import filesizeformat
from django.core.validators import ValidationError, FileExtensionValidator
from User.models import CustomUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.



def validate_image_size(image):
    filesize = image.size
    if filesize > int(settings.MAX_UPLOAD_IMAGE_SIZE):
        raise ValidationError('Max image size should be '.format((filesizeformat(settings.MAX_UPLOAD_IMAGE_SIZE))))
    
def product_image_directory_path(instance, filename):
    return 'Media/product/{0}/pictures/{1}'.format(str(instance.id), filename) 
def toplevel_topic_image_directory_path(instance, filename):
    return 'Media/toplevel_field/{0}/pictures/{1}'.format(str(instance.id), filename) 
def midlevel_topic_image_directory_path(instance, filename):
    return 'Media/midlevel_field/{0}/pictures/{1}'.format(str(instance.id), filename) 
def lowlevel_topic_image_directory_path(instance, filename):
    return 'Media/lowlevel_field/{0}/pictures/{1}'.format(str(instance.id), filename) 
def product_topic_image_directory_path(instance, filename):
    return 'Media/product_field/{0}/pictures/{1}'.format(str(instance.id), filename) 

class ToplevelTopic(models.Model):
    VALID_AVATAR_EXTENSION = ['png', 'jpg', 'jpeg']   

    name=models.CharField(max_length=100,unique=True)
    picture= models.ImageField(upload_to=toplevel_topic_image_directory_path,
                               validators=[FileExtensionValidator(VALID_AVATAR_EXTENSION), validate_image_size],
                               blank=True, null=True, max_length=1000)
    class Meta:
        verbose_name = 'toplevel_topic'
        verbose_name_plural = 'toplevel_topics'
        db_table = 'toplevel_topic'

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_image = self.picture
            self.picture = None
            super(ToplevelTopic, self).save(*args, **kwargs)
            if saved_image:
                self.picture = toplevel_topic_image_directory_path(self,saved_image)
            else:
                self.picture = None
            self.save()
        else:
            super(ToplevelTopic, self).save(*args, **kwargs)

class MidlevelTopic(models.Model):
    VALID_AVATAR_EXTENSION = ['png', 'jpg', 'jpeg']   

    name=models.CharField(max_length=100,unique=True)
    toplevel_topic=models.ForeignKey(ToplevelTopic,on_delete=models.CASCADE,related_name="midlevel_toplevel")
    picture= models.ImageField(upload_to=midlevel_topic_image_directory_path,
                               validators=[FileExtensionValidator(VALID_AVATAR_EXTENSION), validate_image_size],
                               blank=True, null=True, max_length=1000)
    is_product=models.BooleanField(default=True,null=False,blank=False)
    class Meta:
        verbose_name = 'midlevel_topic'
        verbose_name_plural = 'midlevel_topics'
        db_table = 'midlevel_topic'

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_image = self.picture
            self.picture = None
            super(MidlevelTopic, self).save(*args, **kwargs)
            if saved_image:
                self.picture = midlevel_topic_image_directory_path(self,saved_image)
            else:
                self.picture = None
            self.save()
        else:
            super(MidlevelTopic, self).save(*args, **kwargs)

class LowlevelTopic(models.Model):
    VALID_AVATAR_EXTENSION = ['png', 'jpg', 'jpeg']

    name=models.CharField(max_length=100,unique=True)
    midlevel_topic=models.ForeignKey(MidlevelTopic,on_delete=models.CASCADE,related_name="lowlevel_midlevel")
    picture= models.ImageField(upload_to=lowlevel_topic_image_directory_path,
                               validators=[FileExtensionValidator(VALID_AVATAR_EXTENSION), validate_image_size],
                               blank=True, null=True, max_length=1000)
    class Meta:
        verbose_name = 'lowlevel_topic'
        verbose_name_plural = 'lowlevel_topics'
        db_table = 'lowlevel_topic'

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_image = self.picture
            self.picture = None
            super(LowlevelTopic, self).save(*args, **kwargs)
            if saved_image:
                self.picture = lowlevel_topic_image_directory_path(self,saved_image)
            else:
                self.picture = None
            self.save()
        else:
            super(LowlevelTopic, self).save(*args, **kwargs)

class ProductTopic(models.Model):
    VALID_AVATAR_EXTENSION = ['png', 'jpg', 'jpeg']   

    name=models.CharField(max_length=100,unique=True)
    lowlevel_topic=models.ForeignKey(LowlevelTopic,on_delete=models.CASCADE,related_name="product_topic_lowlevel_topic")
    picture= models.ImageField(upload_to=product_topic_image_directory_path,
                               validators=[FileExtensionValidator(VALID_AVATAR_EXTENSION), validate_image_size],
                               blank=True, null=True, max_length=1000)
    class Meta:
        verbose_name = 'product_topic'
        verbose_name_plural = 'product_topics'
        db_table = 'product_topic'

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_image = self.picture
            self.picture = None
            super(ProductTopic, self).save(*args, **kwargs)
            if saved_image:
                self.picture = product_topic_image_directory_path(self,saved_image)
            else:
                self.picture = None
            self.save()
        else:
            super(ProductTopic, self).save(*args, **kwargs)

class StaticField(models.Model):
    name=models.CharField(max_length=100)
    object_id = models.PositiveIntegerField(default=0)
    topic_level=models.IntegerField(default=None)
    is_filter=models.BooleanField(default=False)
    is_choosable=models.BooleanField(default=False)
    class Meta:
        verbose_name = 'static_field'
        verbose_name_plural = 'static_fields'
        db_table = 'static_field'



class FieldValue(models.Model):
    value=models.CharField(max_length=250)
    static_field=models.ForeignKey(StaticField,on_delete=models.CASCADE,related_name="static_filed_value")
    class Meta:
        verbose_name = 'field_value'
        verbose_name_plural = 'field_values'
        db_table = 'field_value'







class Product(models.Model):
    name = models.CharField(max_length=100)
    shop=models.ForeignKey(Shop,on_delete=models.CASCADE, related_name="product_shop")
    product_topic=models.ForeignKey(ProductTopic,on_delete=models.CASCADE, related_name="shop_product_topic")
    is_in_event=models.BooleanField(default=False)
    is_new=models.BooleanField(default=False)
    num_of_seen=models.IntegerField(default=0)
    is_confirm=models.BooleanField(default=False)
    detail=models.CharField(max_length=500,null=True,blank=True)
    rate=models.IntegerField(default=0)
    num_of_rates=models.IntegerField(default=0)
    creator_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="creator_id")
    admin_confirm=models.BooleanField(default=False)
    report_message=models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        db_table = 'product'

class ProductPicture(models.Model):
    VALID_AVATAR_EXTENSION = ['png', 'jpg', 'jpeg']   
    product_pic= models.ImageField(upload_to=product_image_directory_path,
                               validators=[FileExtensionValidator(VALID_AVATAR_EXTENSION), validate_image_size],
                               blank=True, null=True, max_length=1000)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'product_picture'
        verbose_name_plural = 'product_pictures'
        db_table = 'product_picture'

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_image = self.product_pic
            self.product_pic = None
            super(ProductPicture, self).save(*args, **kwargs)
            if saved_image:
                self.product_pic = product_image_directory_path(self,saved_image)
            else:
                self.product_pic = None
            self.save()
        else:
            super(ProductPicture, self).save(*args, **kwargs)

class ProductInstance(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_instance")
    price=models.FloatField(default=0.0)
    discount=models.IntegerField(default=0)
    capacity=models.IntegerField(default=0)

    class Meta:
        verbose_name = 'product_instance'
        verbose_name_plural = 'product_instances'
        db_table = 'product_instance'

class ProductStaticField(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_static_field")
    field=models.ForeignKey(StaticField,on_delete=models.CASCADE,related_name="product_static_field")
    field_value=models.ForeignKey(FieldValue,on_delete=models.CASCADE,related_name="product_static_field",null=True,blank=True)
    value=models.CharField(max_length=250,null=True,blank=True)
    class Meta:
        verbose_name = 'product_static_field'
        verbose_name_plural = 'product_static_fields'
        db_table = 'product_static_field'

class ProductDynamicField(models.Model):
    product_instance=models.ForeignKey(ProductInstance,on_delete=models.CASCADE,related_name="product_dynamic_field")
    field=models.ForeignKey(StaticField,on_delete=models.CASCADE,related_name="product_dynamic_field")
    field_value=models.ForeignKey(FieldValue,on_delete=models.CASCADE,related_name="product_dynamic_field",null=True,blank=True)
    value=models.CharField(max_length=250,null=True,blank=True)
    class Meta:
        verbose_name = 'product_dynamic_field'
        verbose_name_plural = 'product_dynamic_fields'
        db_table = 'product_dynamic_field'

class MidlevelTopicProviderBranch(models.Model):
    midlevel_topic=models.ForeignKey(MidlevelTopic,on_delete=models.CASCADE,related_name="midlevel_topic_provider_branch",null=False,blank=False)
    provider_branch=models.ForeignKey(ProviderBranch,on_delete=models.CASCADE,related_name="provider_branch_midlevel_topic",null=False,blank=False)

    class Meta:
        verbose_name = 'midlevel_topic_provider_branch'
        verbose_name_plural = 'midlevel_topic_provider_branchs'
        db_table = 'midlevel_topic_provider_branch'