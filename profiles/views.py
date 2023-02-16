from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from products.models import Product
from .models import WishList

class AddToWishlistView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        wishlist, created = WishList.objects.get_or_create(user=request.user)
        wishlist.products.add(product)
        # TODO: Add confirmation message to frontend
        return redirect(request.META.get('HTTP_REFERER', 'wish_list'))

class RemoveFromWishlistView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        wishlist, created = WishList.objects.get_or_create(user=request.user)
        wishlist.products.remove(product)
        print("Removed from wishlist")
        # TODO: Add confirmation message to frontend
        return redirect(request.META.get('HTTP_REFERER', 'wish_list'))