from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from .models import Order

class StaffMemberRequiredMixin(UserPassesTestMixin):
    """
    Check is the user a staff member to restrict access
    """

    def test_func(self):
        return self.request.user.is_staff


class OrderDetailView(DetailView):
    model = Order
    template_name = "checkout/order_detail.html"
    context_object_name = "order"

    def get_object(self, queryset=None):
        return get_object_or_404(Order,
                                 order_number=self.kwargs["order_number"])


class StaffOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "profiles/orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        user = self.request.user
        orders = Order.objects.filter().order_by("-updated")
        return orders