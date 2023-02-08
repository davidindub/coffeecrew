from django.contrib import admin
from .models import Product, Brand, Category, Image, Coffee


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "brand", "stock")

    ordering = ("sku",)


class CoffeeAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "country", "harvest_year")


admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Coffee, CoffeeAdmin)
