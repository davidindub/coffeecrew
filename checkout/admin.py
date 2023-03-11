from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    fields = ("product", "quantity", "price")
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    """
    Define properties to be shows in Django admin list
    """
    inlines = (OrderLineItemAdminInline,)
    list_display = ("order_number", "user", "updated",
                    "completed", "grand_total")
    readonly_fields = ("order_number", "user", "updated",
                       "completed", "order_total", "delivery_cost",
                       "delivery_method", "grand_total", "stripe_pid",
                       "shipped_date", "completed")
    ordering = ("-updated",)


class OrderLineItemAdmin(admin.ModelAdmin):
    """
    Define properties to be shows in Django admin list
    """
    list_display = ("product", "quantity")
    readonly_fields = ("order", "product", "quantity",
                       "product", "price", "product_name", "grind_size")


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLineItem, OrderLineItemAdmin)
