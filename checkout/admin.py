from django.contrib import admin
from .models import Order, OrderLineItem


class OrderItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    # readonly_fields = ("total",)
    fields = ("product", "quantity",)


class OrderAdmin(admin.ModelAdmin):
    """
    Define properties to be shows in Django admin list
    """
    inlines = (OrderItemAdminInline,)
    list_display = ("order_number", "user", "updated",
                    "completed", "grand_total")
    readonly_fields = ("order_number", "user", "updated",
                       "completed", "order_total", "delivery_cost",
                       "delivery_method", "grand_total", "stripe_pid",
                       "shipped_date", "completed")
    ordering = ("-updated",)


# class OrderItemAdmin(admin.ModelAdmin):
#     """
#     Define properties to be shows in Django admin list
#     """
#     list_display = ("product", "quantity", "total")
#     readonly_fields = ("order", "product", "quantity",
#                        "product", "price", "product_name", "grind_size",
#                        "total")


admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderItem, OrderItemAdmin)
