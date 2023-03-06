from .models import Cart


def get_cart_for_guest_or_user(request):
    """
    Return the cart for registered users of guests
    """
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        cart = Cart.objects.get(guest_id=request.session["guest_id"])
    return cart
