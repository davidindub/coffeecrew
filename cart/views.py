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

        return render(request,
                      "cart/shopping_cart.html",
                      {"cart_items": items,
                       "cart": cart,
                       "total": total})


class CartAddView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart = Cart.objects.get(user=request.user)
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.get_or_create(
            cart=cart, product=product)
        if not cart_item:
            cart_item.adjust_quantity(cart_item.quantity + 1)
        return redirect('shopping_cart')


class CartRemoveView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart = Cart.objects.get(user=request.user)
        product = Product.objects.get(id=product_id)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        cart_item.adjust_quantity(0)
        return redirect('shopping_cart')


class CartAdjustQuantityView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, product__id=product_id)
        new_quantity = request.POST.get('new_quantity')
        if new_quantity:
            cart_item.adjust_quantity(int(new_quantity))
        else:
            cart_item.adjust_quantity(1)
        return redirect('shopping_cart')