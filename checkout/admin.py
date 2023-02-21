from django.contrib import admin
from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "updated", "completed", "grand_total")


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "total")


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
