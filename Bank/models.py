from django.db import models
from django.template.defaultfilters import filesizeformat
from django.core.validators import ValidationError, FileExtensionValidator
from EvaamBack import settings
# Create your models here.

def validate_image_size(image):
    filesize = image.size
    if filesize > int(settings.MAX_UPLOAD_IMAGE_SIZE):
        raise ValidationError('Max image size should be '.format((filesizeformat(settings.MAX_UPLOAD_IMAGE_SIZE))))
    
def bank_picture_directory_path(instance, filename):
    return 'Media/bank/{0}/pictures/{1}'.format(str(instance.id), filename) 
class Bank(models.Model):
    VALID_AVATAR_EXTENSION = ['png', 'jpg', 'jpeg']   

    name=models.CharField(max_length=100,null=False,blank=False)
    picture= models.ImageField(upload_to=bank_picture_directory_path,
                               validators=[FileExtensionValidator(VALID_AVATAR_EXTENSION), validate_image_size],
                               blank=True, null=True, max_length=1000)
    class Meta:
        verbose_name = 'bank'
        verbose_name_plural = 'banks'
        db_table = 'bank'


class Facility(models.Model):
    name=models.CharField(max_length=100,null=False,blank=False)
    bank=models.ForeignKey(Bank,on_delete=models.CASCADE,related_name="bank_id_facility")
    max_value=models.CharField(max_length=100,null=False,blank=False)
    evaam_subscripton_percent=models.FloatField(default=3.5)
    pre_payment_percent=models.FloatField(default=3.5)
    bank_interest_percent=models.FloatField(default=23)
    class Meta:
        verbose_name = 'facility'
        verbose_name_plural = 'facilities'
        db_table = 'facility'

class FacilityDocument(models.Model):
    name=models.CharField(max_length=100,null=False,blank=False)
    facility=models.ForeignKey(Facility,on_delete=models.CASCADE,related_name="facility_id_facility_document")
    type=models.CharField(max_length=100,null=False,blank=False)
    class Meta:
        verbose_name = 'facility_document'
        verbose_name_plural = 'facility_documents'
        db_table = 'facility_document'