from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from .models import Order


class OrderDetailView(DetailView):
    model = Order
    template_name = "checkout/order_detail.html"
    context_object_name = "order"

    def get_object(self, queryset=None):
        return get_object_or_404(Order,
                                 order_number=self.kwargs["order_number"])
