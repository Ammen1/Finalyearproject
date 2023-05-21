from django.contrib import admin

from .models import  Promotion, PromoType,ProductsOnPromotion, Coupon,ProductInventory

admin.site.register(Promotion),
admin.site.register(ProductInventory),
admin.site.register(PromoType),
admin.site.register(Coupon),
admin.site.register(ProductsOnPromotion),

