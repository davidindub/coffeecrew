from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, FormView
from products.models import Product
from .models import WishList, Profile, Address
from cart.models import Cart, CartItem
from checkout.models import Order, OrderItem
from .forms import ProfileForm


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "profiles/customer_dashboard.html"

    def get_recent_orders(self):
        user = self.request.user
        return Order.objects.filter(user=user).order_by("-updated")[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = Profile.objects.get(user=self.request.user)
        context["profile"] = profile

        # Get the user's orders and add them to the context
        orders = Order.objects.filter(user=self.request.user)
        context["orders"] = orders

        shipping_address = Address.objects.filter(
            profile=profile, order__isnull=True)
        billing_address = Address.objects.filter(
            profile=profile, order__isnull=True)
        context["shipping_address"] = shipping_address.first()
        context["billing_address"] = billing_address.first()

        recent_orders = self.get_recent_orders()
        context["recent_orders"] = recent_orders

        return context


class ProfileUpdateView(LoginRequiredMixin, FormView):
    template_name = "profiles/forms/profile_form.html"
    form_class = ProfileForm
    success_url = "account_dashboard"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.request.user.profile
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AddToWishlistView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        wishlist, created = WishList.objects.get_or_create(user=request.user)
        wishlist.products.add(product)
        # TODO: Add confirmation message to frontend
        return redirect(request.META.get("HTTP_REFERER", "wish_list"))


class RemoveFromWishlistView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        wishlist, created = WishList.objects.get_or_create(user=request.user)
        wishlist.products.remove(product)
        # TODO: Add confirmation message to frontend
        return redirect(request.META.get('HTTP_REFERER', 'wish_list'))
