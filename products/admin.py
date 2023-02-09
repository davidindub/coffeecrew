from django.contrib import admin
from .models import Product, Brand, Category, Coffee, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "brand", "stock")
    inlines = [ProductImageInline]
    ordering = ("sku",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("friendly_name", "name")

    ordering = ("friendly_name",)


class CoffeeAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "country", "harvest_year")
    inlines = [ProductImageInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
admin.site.register(ProductImage)
admin.site.register(Coffee, CoffeeAdmin)
