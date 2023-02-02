from django.shortcuts import get_object_or_404, render
from django.views import generic, View
from .models import Product, Coffee


def all_products(request):
    """
    renders view for all products, including sorting and searching
    """
    products = Product.objects.all()

    context = {"products": products}
    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """
    renders view for an single products full details
    """
    product = get_object_or_404(Product, pk=product_id)

    context = {"product": product}
    return render(request, "products/product_detail.html", context)


# class ProductsList(generic.ListView):
#     model = Product
#     template_name = "products/products.html"

#     def get_queryset(self):
#         query_set = super().get_queryset()

#         query_set = query_set.filter(visible_to_customers=True)

#         return query_set

#     def get_context_data(self, **kwargs):
#         return super().get_context_data(**kwargs)
