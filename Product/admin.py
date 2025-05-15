from django.contrib import admin
from .models import ToplevelTopic,MidlevelTopic,LowlevelTopic,Product,ProductTopic,ProductPicture,ProductInstance,ProductStaticField,ProductDynamicField,ProviderBranch,MidlevelTopicProviderBranch
# Register your models here.
admin.site.register(ToplevelTopic)
admin.site.register(MidlevelTopic)
admin.site.register(LowlevelTopic)
admin.site.register(Product)
admin.site.register(ProductTopic)
admin.site.register(ProductPicture)
admin.site.register(ProductInstance)
admin.site.register(ProductStaticField)
admin.site.register(ProductDynamicField)
admin.site.register(ProviderBranch)
admin.site.register(MidlevelTopicProviderBranch)
