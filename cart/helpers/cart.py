from cart.models import Cart, CartItem


def get_cart_for_guest_or_user(request):
    """
    Return the cart for registered users of guests
    """
    if request.user.is_authenticated:
        return Cart.objects.get(user=request.user)
    elif request.COOKIES.get("guest_id"):
        cart, created = Cart.objects.get_or_create(
            guest_id=request.COOKIES.get("guest_id"))
        return cart
    else:
        return None


def move_guest_cart_to_user_cart(request, user):
    # Retrieve the guest cart based on the session key stored in the request
    guest_id = request.COOKIES.get("guest_id")

    try:
        guest_cart = Cart.objects.get(guest_id=guest_id)
    except Cart.DoesNotExist:
        return

    # Create or retrieve the user's cart
    user_cart, created = Cart.objects.get_or_create(user=user)

    # Copy each item from the guest cart to the user cart
    for guest_item in guest_cart.cart_item.all():
        # Check if the item is already in the user cart
        user_item, created = CartItem.objects.get_or_create(
            cart=user_cart, product=guest_item.product
        )
        if not created:
            # Update the quantity of the item in the user cart
            user_item.quantity = user_item.quantity + guest_item.quantity
        else:
            user_item.quantity = guest_item.quantity
        user_item.save()

    # Delete the guest cart
    guest_cart.delete()
