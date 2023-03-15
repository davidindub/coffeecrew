from django.contrib import admin
from django.contrib import admin
from .models import WishList, Profile, Address


class WishListAdmin(admin.ModelAdmin):
    """
    Define properties to be shown in Django admin list
    """
    list_display = ("user", "num_products")
    readonly_fields = ("user", "num_products")


class ProfileAdmin(admin.ModelAdmin):
    """
    Define properties to be shown in Django admin list
    """
    list_display = ("user", "shipping_address", "billing_address")
    readonly_fields = ("user", "shipping_address", "billing_address")


class AddressAdmin(admin.ModelAdmin):
    """
    Define properties to be shown in Django admin list
    """
    list_display = ("profile", "address_line_1")


admin.site.register(WishList, WishListAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Address, AddressAdmin)
