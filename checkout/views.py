import os
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (DetailView, ListView,
                                  View, TemplateView, FormView)
from django.db import IntegrityError
from .models import Order, OrderLineItem
from cart.models import CartItem, Cart
from .forms import CheckoutAddressForm
from profiles.models import Profile
import stripe
from coffeecrew.settings import (STRIPE_PUBLIC_KEY,
                                 STRIPE_SECRET_KEY, STRIPE_CURRENCY)
from cart.get_cart import get_cart_for_guest_or_user


stripe.api_key = STRIPE_SECRET_KEY


class StaffMemberRequiredMixin(UserPassesTestMixin):
    """
    Check is the user a staff member to restrict access
    """

    def test_func(self):
        return self.request.user.is_staff


class OrderDetailView(LoginRequiredMixin, DetailView):
    """
    View for showing full details of an order
    """
    model = Order
    template_name = "checkout/order_detail.html"
    context_object_name = "order"

    def get_object(self, queryset=None):
        return get_object_or_404(Order,
                                 order_number=self.kwargs["order_number"])


class OrderDispatchView(StaffMemberRequiredMixin, View):
    """
    View for showing setting an order as dispatched,
    redirects to the Order Detail View
    """

    def get(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number)
        try:
            order.set_as_shipped()
            messages.success(
                self.request, f"Order {order.order_number} dispatched!")
        except Order.DoesNotExist:
            messages.error(self.request, "Order does not exist")

        return redirect(reverse("order_detail",
                                kwargs={'order_number': order.order_number}))


class StaffOrderListView(StaffMemberRequiredMixin, ListView):
    """
    View for Staff view list of orders
    """
    model = Order
    template_name = "profiles/orders.html"
    context_object_name = "orders"
    # paginate_by = 20

    def get_queryset(self):
        queryset = Order.objects.filter().order_by("-updated")

        if self.request.GET.get("dispatched") == "false":
            queryset = queryset.filter(shipped_date__isnull=True)
        if self.request.GET.get("dispatched") == "true":
            queryset = queryset.filter(shipped_date__isnull=False)

        return queryset


class CheckoutReviewView(ListView):
    """
    View for users to review their order before starting Checkout
    """
    model = CartItem
    template_name = "checkout/step_1_review_items.html"
    context_object_name = "cart_items"
    ordering = ["-date_added"]

    def get_queryset(self):
        queryset = self.model.objects.filter(
            cart=get_cart_for_guest_or_user(self.request))
        queryset = queryset.order_by("date_added", "id")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["checkout_step"] = "review"
        return context


class CheckOutShippingView(LoginRequiredMixin, FormView):
    """
    View for users to enter their delivery address
    """
    form_class = CheckoutAddressForm
    template_name = "checkout/step_2_shipping.html"
    success_url = reverse_lazy("checkout_payment")

    def form_valid(self, form):
        order, created = Order.objects.get_or_create(
            user=self.request.user,
            completed=False
        )
        cart = get_object_or_404(Cart, user=self.request.user)

        if created:
            print("NEW ORDER CREATED")
        else:
            print(f"UPDATING EXISTING ORDER {order.order_number}")

        address = form.cleaned_data

        print(address)
        print("UPDATING ADDRESS:")
        print(address["full_name"])

        order.full_name = address["full_name"]
        order.address_line_1 = address["address_line_1"]
        order.address_line_2 = address["address_line_2"]
        order.city = address["city"]
        order.postcode = address["postcode"]
        order.country = address["country"]
        order.save()

        print(f"full name in order: {order.full_name}")

        if not created:
            print("Deleting existing Order line items")
            order.order_items.all().delete()

        for item in cart.cart_item.all():
            print("adding new order line items")
            OrderLineItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                product_name=item.product.name,
                grind_size=item.grind_size,
            )
        order.save()

        if created:
            print(f"New order {order.order_number} created")
        else:
            print(f"Order {order.order_number} updated.")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # context["cart"] = Cart.objects.get(user=user)
        context["checkout_step"] = "delivery"

        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=user)
            default_shipping = profile.shipping_address
            if default_shipping:
                context["full_name"] = user.get_full_name()
                context["address_line_1"] = default_shipping.address_line_1
                context["address_line_2"] = default_shipping.address_line_2
                context["address_city"] = default_shipping.city
                context["address_postcode"] = default_shipping.postcode
                context["address_country"] = default_shipping.country.code

        return context


class CheckoutPaymentView(LoginRequiredMixin, TemplateView):
    """
    View for users to select a payment method
    """
    template_name = "checkout/step_3_payment.html"

    def get_context_data(self, **kwargs):
        """
        Pass context to payment template
        """
        context = super().get_context_data(**kwargs)

        if not STRIPE_PUBLIC_KEY:
            messages.warning(request, "Stripe Public Key Missing!!")

        # cart = get_object_or_404(Cart, user=self.request.user)
        order = get_object_or_404(Order, user=self.request.user,
                                  completed=False)
        stripe_total = round(order.grand_total * 100)
        print(f"stripe total is {stripe_total}")

        if not order.stripe_pid:
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=STRIPE_CURRENCY,
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            print(f"Intent created {intent.id}")
            # Save created payment intent to order
            order.stripe_pid = intent.id
            order.save()
        else:
            # Update the intent on stripe
            intent = stripe.PaymentIntent.modify(
                order.stripe_pid, amount=stripe_total)
            print(f"Intent updated on stripe {intent.id}")

        context["user"] = self.request.user
        context["user_fullname"] = self.request.user.get_full_name
        context["checkout_step"] = "payment"
        context["stripe_public_key"] = STRIPE_PUBLIC_KEY
        context["client_secret"] = intent.client_secret
        context["order"] = order
        return context


class SuccessView(TemplateView):
    template_name = "checkout/step_4_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart = get_object_or_404(Cart, user=self.request.user)
        order = get_object_or_404(Order, user=self.request.user,
                                  completed=False)

        print(f"order no: {order}")
        print(f"order stripe pid: {order.stripe_pid}")

        client_secret = self.request.GET.get(
            "payment_intent_client_secret")
        print(f"client_secret status: {client_secret}")

        payment_status = stripe.PaymentIntent.retrieve(order.stripe_pid).status
        print(f"payment status: {payment_status}")

        if payment_status == "succeeded":
            context["success"] = True
            print("PAYMENT SUCCESSFUL")

            cart.reset_cart_after_sale()
            print("CART RESET")

            order.complete_order()
            print("SETTING ORDER AS COMPLETE")

            context["checkout_step"] = "complete"
            # TODO: Send customer email

            context["order"] = order
            return context

        else:
            context["success"] = False
            print("Payment NOT successful")

            context["checkout_step"] = "payment"
            return redirect("payment_failure")

        context["order"] = order
        return context


class PaymentFailedView(TemplateView):
    template_name = "checkout/step_4_failure.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["success"] = False
        print("Payment NOT successful")

        return context


class CancelView(TemplateView):
    template_name = "cancel.html"
