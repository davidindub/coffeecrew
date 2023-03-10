from django.shortcuts import get_object_or_404, render, reverse
from django.views.generic import ListView
from django.contrib import messages
from profiles.models import WishList
from .models import Product, Category, Department, Brand


# Views related to Products:

class ProductsListView(ListView):
    """
    renders view for all products, including sorting and searching
    """
    model = Product
    template_name = "products/products.html"
    context_object_name = "products"
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()

        wishlist = self.kwargs.get("wishlist")
        department = self.kwargs.get("department")
        category = self.kwargs.get("category")
        brand = self.kwargs.get("brand")
        query = self.request.GET.get("search", None)

        sort = self.request.GET.get("sort")
        order = self.request.GET.get("order")

        if wishlist:
            wishlist = get_object_or_404(WishList, user=self.request.user)
            queryset = wishlist.products.all()

        if department:
            queryset = queryset.filter(
                category__department__name=department).distinct()

        if category:
            queryset = queryset.filter(
                category__name=category).distinct()

        if brand:
            queryset = queryset.filter(brand__name=brand)

        if query:
            queryset = queryset.filter(name__icontains=query
                                       ).distinct() | queryset.filter(
                description__icontains=query).distinct()

        elif query == "":
            messages.error(self.request,
                           "You didn't enter any search criteria.")

            queryset = queryset.none()

        if sort == "name":
            if order == "asc":
                queryset = queryset.order_by("name")
            else:
                queryset = queryset.order_by("-name")
        elif sort == "price":
            if order == "asc":
                queryset = queryset.order_by("price")
            else:
                queryset = queryset.order_by("-price")
        elif sort == "date_added":
            if order == "asc":
                queryset = queryset.order_by("date_added")
            else:
                queryset = queryset.order_by("-date_added")

        return queryset.filter(visible_to_customers=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        wishlist = self.kwargs.get("wishlist")
        department = self.kwargs.get("department")
        category = self.kwargs.get("category")
        brand = self.kwargs.get("brand")
        query = self.request.GET.get("search", None)

        sort = self.request.GET.get("sort")
        order = self.request.GET.get("order")

        page_number = self.request.GET.get("page")

        # Add the current sorting order as a query
        # parameter to pagination links

        if page_number:
            pagination_links = context["paginator"].get_elided_page_range(
                number=page_number, on_each_side=2)
            pagination_links = [
                f'{reverse("products")}?{self.request.GET.urlencode()}&page={i}' for i in pagination_links]  # noqa
        else:
            pagination_links = context["paginator"].get_elided_page_range(
                on_each_side=2)
            pagination_links = [
                f'{reverse("products")}?{self.request.GET.urlencode()}&page={i}' for i in pagination_links]  # noqa

        if sort == "name":
            if order == "asc":
                context["sort_selected"] = "Name (A-Z)"
            else:
                context["sort_selected"] = "Name (Z-A)"
        elif sort == "price":
            if order == "asc":
                context["sort_selected"] = "Price (Low to High)"
            else:
                context["sort_selected"] = "Price (High to Low)"
        elif sort == "date_added":
            if order == "asc":
                context["sort_selected"] = "Oldest First"
            else:
                context["sort_selected"] = "Newest First"

        context["category"] = get_object_or_404(
            Category, name=category) if category else None

        context["department"] = get_object_or_404(
            Department, name=department) if department else None

        context["brand"] = get_object_or_404(
            Brand, name=brand) if brand else None

        if wishlist:
            context["wishlist_page"] = True

        context["search_results"] = query

        return context


def product_detail(request, slug):
    """
    View for an single products full details
    """
    product = get_object_or_404(Product, slug=slug)

    context = {"product": product}
    return render(request, "products/product_detail.html", context)
