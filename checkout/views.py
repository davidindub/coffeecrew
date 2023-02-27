from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView, View
from .models import Order


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

    def get_queryset(self):
        orders = Order.objects.filter().order_by("-updated")
        return orders
