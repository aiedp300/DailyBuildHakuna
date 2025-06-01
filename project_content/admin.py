from django.contrib import admin
from .models import *
#from project_content.models import *

# class ProductImageInline(admin.TabularInline):
#     model = ProductImage

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     inlines = [
#         ProductImageInline,
#     ]

# admin.site.register(ProductImage)


class UnitImageInline(admin.TabularInline):
    model = UnitImage

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    inlines = [
        UnitImageInline,
    ]

admin.site.register(UnitImage)
admin.site.register(Venue),
admin.site.register(Location),
admin.site.register(UnitSite),
admin.site.register(UnavailableDate),
admin.site.register(Product),
admin.site.register(Purchase),
admin.site.register(ServicePurchase),
#admin.site.register(Booking),