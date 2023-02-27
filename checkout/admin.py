from django.contrib import admin
from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    """
    Define properties to be shows in Django admin list
    """
    list_display = ("order_number", "user", "updated",
                    "completed", "grand_total")


class OrderItemAdmin(admin.ModelAdmin):
    """
    Define properties to be shows in Django admin list
    """
    list_display = ("product", "quantity", "total")


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
