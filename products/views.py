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

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()

        # print(f"✅✅✅ {kwargs.category}")

        category = self.kwargs.get('category')
        query = self.request.GET.get('search', None)
        sort = self.request.GET.get('sort')
        order = self.request.GET.get('order')

        if category:
            queryset = queryset.filter(
                category__name=category).distinct()

        if query:
            queryset = queryset.filter(name__icontains=query
                                       ).distinct() | queryset.filter(
                description__icontains=query).distinct()

        elif query == "":
            messages.error(self.request,
                           "You didn't enter any search criteria.")
            # print("You didn't enter any search criteria.")

            queryset = queryset.none()

        if sort == 'name':
            if order == 'asc':
                queryset = queryset.order_by('name')
            else:
                queryset = queryset.order_by('-name')
        elif sort == 'price':
            if order == 'asc':
                queryset = queryset.order_by('price')
            else:
                queryset = queryset.order_by('-price')
        elif sort == 'date_added':
            if order == 'asc':
                queryset = queryset.order_by('date_added')
            else:
                queryset = queryset.order_by('-date_added')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = self.kwargs.get('category')

        context["category"] = get_object_or_404(
            Category, name=category) if category else None

        return context


def product_detail(request, product_id):
    """
    renders view for an single products full details
    """
    product = get_object_or_404(Product, pk=product_id)

    context = {"product": product}
    return render(request, "products/product_detail.html", context)
