from django.contrib import admin
from .models import CustomUser,CreditWallet,Address,JibitToken,UserCreditTransaction
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(CreditWallet)
admin.site.register(Address)
admin.site.register(JibitToken)
admin.site.register(UserCreditTransaction)
