from django.contrib import admin
from .models import Bank,Facility,FacilityDocument,FacilityInstallmentNumber,UserDocumetn,UserFacility,UserInstallment,Grade,SubGrade
# Register your models here.
admin.site.register(Bank)
admin.site.register(Facility)
admin.site.register(FacilityDocument)
admin.site.register(FacilityInstallmentNumber)
admin.site.register(UserDocumetn)       
admin.site.register(UserFacility)
admin.site.register(UserInstallment)
admin.site.register(Grade)
admin.site.register(SubGrade)