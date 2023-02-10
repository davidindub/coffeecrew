from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from products.models import Product
from .models import Cart, CartItem
from django.views import generic, View


class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        items = cart.cartitem_set.all()
        total = sum(item.product.price * item.quantity for item in items)
        return render(request, 'cart/shopping_cart.html', {'cart_items': items,
                                                           "total": total})


class CartAddView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart = Cart.objects.get(user=request.user)
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('shopping_cart')


class CartRemoveView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart = Cart.objects.get(user=request.user)
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('shopping_cart')
