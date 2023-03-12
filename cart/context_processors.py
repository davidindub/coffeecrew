from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import uuid
from .models import Cart, CartItem
from .helpers.cart import get_cart_for_guest_or_user


def cart_total(request):
    cart = None
    try:
        cart = get_cart_for_guest_or_user(request)
    except KeyError as e:
        # Guest cart not yet created, let cart() create cookie and cart first
        print(e)
    finally:
        return {"cart_total": cart.total() if cart else 0.00}


def cart(request):
    if request.user.is_authenticated:
        return {"cart": Cart.objects.get(user=request.user)}

    guest_id = request.COOKIES.get("guest_id")
    try:
        cart = Cart.objects.get(guest_id=guest_id)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(guest_id=guest_id)
    print("It worked")
    return {"cart": cart}
