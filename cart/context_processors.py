from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import uuid
from .models import Cart, CartItem
from .helpers.cart import get_cart_for_guest_or_user


def cart_total(request):
    cart = None
    try:
        cart = get_cart_for_guest_or_user(request)
    finally:
        return {"cart_total": cart.total() if cart else 0.00}


def cart(request):
    if request.user.is_authenticated:
        return {"cart": Cart.objects.get(user=request.user)}

    guest_id = request.COOKIES.get("guest_id")
    if guest_id:
        cart = Cart.objects.get_or_create(guest_id=guest_id)
        return {"cart": cart}

    if not guest_id:
        return {"cart": None}
