from .models import Cart


def cart_total(request):
    cart = None
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    return {"cart_total": cart.total() if cart else 0.00}
