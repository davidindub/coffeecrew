from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.views import generic, View
from django.contrib import messages
from django.db.models import Q
from .models import Product, Coffee, Category


class ProductsList(generic.ListView):
    """
    renders view for all products, including sorting and searching
    """
    model = Product
    template_name = "products/products.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset()

        category = self.request.GET.get('category', None)
        query = self.request.GET.get('search', None)

        if category:
            categories = category.split(",")
            queryset = queryset.filter(category__name__in=categories)

            return queryset

        if query:
            print(f"searching for {query}")

            queryset = queryset.filter(name__icontains=query
                                       ) | queryset.filter(
                description__icontains=query)
            return queryset

        elif query == "":
            messages.error(self.request,
                           "You didn't enter any search criteria.")
            print("You didn't enter any search criteria.")

            return queryset.none()

        return queryset


def product_detail(request, product_id):
    """
    renders view for an single products full details
    """
    product = get_object_or_404(Product, pk=product_id)

    context = {"product": product}
    return render(request, "products/product_detail.html", context)
