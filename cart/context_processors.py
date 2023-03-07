from django.core.exceptions import ObjectDoesNotExist
import uuid
from .models import Cart
from .get_cart import get_cart_for_guest_or_user


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
        print("got user cart!")
        return {"cart": Cart.objects.get(user=request.user)}
    else:
        try:
            guest_id = request.session["guest_id"]
        except KeyError:
            print("storing id in session")
            request.session["guest_id"] = str(uuid.uuid4())
            guest_id = request.session["guest_id"]
            print("stored in session")

        cart = Cart.objects.get_or_create(guest_id=guest_id)
        print("got guest cart!")

        return {"cart": cart}
