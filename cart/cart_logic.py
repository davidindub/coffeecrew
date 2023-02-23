from django.conf import settings
from decimal import Decimal


def calculate_delivery_cost(cart_total):
    if cart_total < settings.FREE_DELIVERY_THRESHOLD:
        return (settings.DELIVERY_COST).quantize(Decimal("0.01"))
    else:
        return Decimal(0.00)


def is_free_delivery(cart_total):
    return cart_total > settings.FREE_DELIVERY_THRESHOLD


def get_spend_for_free_delivery(cart_total):
    return settings.FREE_DELIVERY_THRESHOLD - (cart_total)


def calculate_total_with_delivery(cart_total):
    total = (cart_total) + calculate_delivery_cost(cart_total)
    return total.quantize(Decimal("0.01"))
