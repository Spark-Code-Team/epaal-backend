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
    nickname=models.CharField(max_length=100,null=True,blank=True)
    jiibit_bank_naem=models.CharField(max_length=100,null=False,blank=False)
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

class Grade(models.Model):
    name=models.CharField(max_length=100,null=False,blank=False)

class SubGrade(models.Model):
    name=models.CharField(max_length=100,null=False,blank=False)
    grade=models.ForeignKey(Grade,on_delete=models.CASCADE,related_name="grade_id_sub_grade")

class FacilityInstallmentNumber(models.Model):
    facility=models.ForeignKey(Facility,on_delete=models.CASCADE,related_name="facility_id_facility_installment_number")
    number_of_installment=models.IntegerField()
    class Meta:
        verbose_name = 'facility_installment_number'
        verbose_name_plural = 'facility_installment_numbers'
        db_table = 'facility_installment_number'

class UserFacility(models.Model):
    user=models.ForeignKey('User.CustomUser',on_delete=models.CASCADE,related_name="user_id_user_facility")
    facility=models.ForeignKey(Facility,on_delete=models.CASCADE,related_name="facility_id_user_facility")
    status=models.CharField(max_length=100)
    max_value=models.CharField(max_length=100,null=False,blank=False)
    evaam_subscripton_percent=models.FloatField(default=3.5)
    pre_payment_percent=models.FloatField(default=3.5)
    bank_interest_percent=models.FloatField(default=23)
    level=models.CharField(max_length=100)
    level_number=models.IntegerField()
    given_value=models.CharField(max_length=100)
    choosen_value=models.CharField(max_length=100)
    sub_grade=models.ForeignKey(SubGrade,on_delete=models.CASCADE,related_name="sub_grade_id_user_facility",null=True,blank=True)
    choosen_facility_installment_number=models.ForeignKey(FacilityInstallmentNumber,on_delete=models.CASCADE,related_name="facility_installment_number_id_user_facility")
    sheba_number=models.CharField(max_length=26,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'user_facility'
        verbose_name_plural = 'user_facilities'
        db_table = 'user_facility'


class UserDocumetn(models.Model):
    user_facility=models.ForeignKey(UserFacility,on_delete=models.CASCADE,related_name="user_facility_id_user_document")
    document=models.ForeignKey(FacilityDocument,on_delete=models.CASCADE,related_name="facility_document_id_user_document")
    value=models.CharField(max_length=100,null=True,blank=True)
    file=models.FileField(upload_to='Media/user_document/',blank=True, null=True, max_length=1000)
    status=models.CharField(max_length=100)
    problem_text=models.CharField(max_length=1000,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'user_document'
        verbose_name_plural = 'user_documents'
        db_table = 'user_document'