from django.shortcuts import get_object_or_404, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView
from products.models import Product
from .models import WishList, Profile, Address
from cart.models import Cart, CartItem
from checkout.models import Order, OrderItem
from .forms import ProfileForm, UserForm
from django.contrib import messages
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


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

        shipping_address = profile.shipping_address
        billing_address = profile.billing_address
        context["shipping_address"] = shipping_address
        context["billing_address"] = billing_address

        recent_orders = self.get_recent_orders()
        context["recent_orders"] = recent_orders

        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "profiles/forms/profile_form.html"
    success_url = reverse_lazy("account_dashboard")

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_form"] = UserForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        messages.success(self.request, "Profile updated!")
        user_form = UserForm(self.request.POST, instance=self.request.user)
        if user_form.is_valid():
            user_form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "There was problem updating your profile!")
        response = super().form_invalid(form)
        response.status_code = 400
        return response


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "profiles/orders.html"
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        orders = Order.objects.filter(user=user).order_by("-updated")
        return orders


class AddressUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Address
    fields = ["address_line_1", "address_line_2",
              "city", "postcode", "country"]
    template_name = "profiles/forms/profile_form.html"

    def test_func(self):
        address = self.get_object()
        return address.profile.user == self.request.user

    def get_form_action(self):
        return reverse("update_account")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        helper = FormHelper()
        helper.form_method = "post"
        helper.form_action = self.get_form_action()
        helper.add_input(Submit("submit", "Update", css_class="btn, btn-cc"))
        form.helper = helper
        return form

    def get_queryset(self):
        return super().get_queryset().filter(profile__user=self.request.user)

    def get_success_url(self):
        messages.success(self.request, "Address updated!")
        return reverse_lazy("account_dashboard")


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
        return redirect(request.META.get("HTTP_REFERER", "wish_list"))
