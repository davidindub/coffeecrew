from django.shortcuts import render
from .models import Product, Coffee


def all_products(request):
    """
    renders view for all products, including sorting and searching
    """
    products = Product.objects.all()

    context = {"products": products}
    return render(request, "products/products.html", context)
