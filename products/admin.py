from django.contrib import admin
from .models import Product, Brand, Category, Coffee, ProductImage, Department


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "brand", "stock")
    inlines = [ProductImageInline]
    ordering = ("sku",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("display_name", "department")

    ordering = ("display_name",)


class CoffeeAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "country", "harvest_year")
    inlines = [ProductImageInline]


admin.site.register(Department)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
admin.site.register(Product, ProductAdmin)
admin.site.register(Coffee, CoffeeAdmin)
admin.site.register(ProductImage)
