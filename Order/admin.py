from django.contrib import admin
from .models import Cart,CartItem,BoughtOrder,Order
# Register your models here.
admin.site.register(Order)
admin.site.register(BoughtOrder)
admin.site.register(Cart)
admin.site.register(CartItem)
