from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from products.models import Product
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from .models import Cart, CartItem
from .helpers.cart import get_cart_for_guest_or_user


class CartView(ListView):
    model = CartItem
    template_name = "cart/shopping_cart.html"
    context_object_name = "cart_items"
    ordering = ["-date_added"]

    def dispatch(self, request, *args, **kwargs):
        if not get_cart_for_guest_or_user(self.request):
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.model.objects.filter(
            cart=get_cart_for_guest_or_user(self.request))

        queryset = queryset.order_by("date_added", "id")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_cart_for_guest_or_user(self.request)

        for item in cart.cart_item.all():
            if item.product.stock == 0:
                # If the item's quantity is zero, remove it from the cart
                messages.error(self.request,
                               (f"{ item.product.name } is out of stock,"
                                " so we've removed it from your cart."))
                item.delete()
            elif item.quantity > item.product.stock:
                # If the item's quantity is greater than the available stock,
                # set the quantity to the available stock
                messages.error(self.request,
                               (f"We don't have enough of {item.product.name}"
                                " to fulfill your order at the moment,"
                                " so we've reduced the quantity."))
                item.quantity = item.product.stock
                item.save()

        return context


class CartAddView(View):
    def post(self, request, product_id):

        cart = get_cart_for_guest_or_user(self.request)

        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product)

        if not created:
            messages.info(self.request,
                          f"{cart_item.product.name} added")
            success = cart_item.adjust_quantity(cart_item.quantity + 1)

            if not success:
                messages.error(self.request,
                               "Sorry, we don't have any more in stock!")

        return redirect("shopping_cart")


class CartRemoveView(View):
    def post(self, request, product_id):
        cart = get_cart_for_guest_or_user(self.request)
        product = Product.objects.get(id=product_id)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        cart_item.adjust_quantity(0)
        return redirect("shopping_cart")


class CartAdjustQuantityView(View):
    def post(self, request, product_id):
        cart = get_cart_for_guest_or_user(self.request)
        cart_item = CartItem.objects.get(cart=cart, product__id=product_id)
        new_quantity = int(request.POST.get("new_quantity"))

        if new_quantity or new_quantity == 0:
            success = cart_item.adjust_quantity(int(new_quantity))

            if not success:
                messages.error(self.request,
                               "Sorry, we don't have any more in stock!")

        return redirect("shopping_cart")


class UpdateCartItemGrindSize(View):
    def post(self, request, product_id, *args, **kwargs):
        cart = get_cart_for_guest_or_user(self.request)
        product = Product.objects.get(id=product_id)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)

        grind_size = request.POST.get("grind_size")

        if cart_item.product.coffee:
            cart_item.grind_size = grind_size
            cart_item.save()
            data = {"success": True}
        else:
            data = {"success": False, "message": "This product is not coffee."}

        return redirect("shopping_cart")
