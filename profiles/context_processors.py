from .models import WishList
from django.shortcuts import get_object_or_404


def get_user_wishlist(request):
    if request.user.is_authenticated:
        try:
            wishlist = get_object_or_404(WishList, user=request.user)
        except WishList.DoesNotExist:
            wishlist = None
    else:
        wishlist = None

    return {"wishlist": wishlist}
