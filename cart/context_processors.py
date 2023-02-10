from .models import Cart


def cart_count(request):
    cart = None
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    return {'cart_count': cart.item_count if cart else 0}
