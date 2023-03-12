from allauth.account.adapter import DefaultAccountAdapter
from .helpers.cart import move_guest_cart_to_user_cart


class MyAccountAdapter(DefaultAccountAdapter):
    def login(self, request, user):
        super().login(request, user)
        move_guest_cart_to_user_cart(request, user)
