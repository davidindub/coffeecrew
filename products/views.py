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

        if query:
            print(f"searching for {query}")

            queryset = queryset.filter(name__icontains=query
                                       ) | queryset.filter(
                description__icontains=query)

        elif query == "":
            messages.error(self.request,
                           "You didn't enter any search criteria.")
            print("You didn't enter any search criteria.")

            queryset = queryset.none()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = self.request.GET.get('category', None)
        categories = []

        if category:
            categories = category.split(",")

        categories = Category.objects.filter(
            name__in=categories).values('friendly_name')

        context["current_categories"] = categories

        return context


def product_detail(request, product_id):
    """
    renders view for an single products full details
    """
    product = get_object_or_404(Product, pk=product_id)

    context = {"product": product}
    return render(request, "products/product_detail.html", context)
