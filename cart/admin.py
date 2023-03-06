from django.contrib import admin
from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "updated")


class CartItemAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity")


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
