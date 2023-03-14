from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DeleteView, View
from django.views.generic.edit import UpdateView, CreateView, FormView
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from coffeecrew.StaffMemberRequiredMixin import StaffMemberRequiredMixin
from products.models import Product, Coffee, Category, Department, Brand
from cart.models import Cart
from checkout.models import Order
from checkout.emails import send_dispatch_email
from .forms import (ProductForm, CoffeeForm, DepartmentForm,
                    CategoryForm, PurgeStaleCartsForm)


class ManageShopView(StaffMemberRequiredMixin, ListView):
    """
    View for management dash
    """
    template_name = "staff/manage_shop.html"
    queryset = Department.objects.all()
    context_object_name = "departments"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        departments = context["departments"]
        context["brands"] = Brand.objects.all().order_by("name")
        context["orders"] = Order.objects.filter().count()
        context["orders_dispatched"] = Order.objects.filter(
            shipped_date__isnull=False).count()
        context["orders_to_dispatch"] = Order.objects.filter(
            shipped_date__isnull=True).count()
        context["total_users"] = User.objects.count()
        context["num_guest_carts"] = Cart.objects.filter(
            guest_id__isnull=False).count()
        context["stale_guest_carts"] = Cart.objects.filter(
            guest_id__isnull=False,
            updated__lt=timezone.now()-timezone.timedelta(weeks=2)).count()

        for department in departments:
            department.categories = Category.objects.filter(
                department=department).order_by("name")
        return context


class ProductUpdateView(StaffMemberRequiredMixin, UpdateView):
    """
    View for updating existing Products
    """
    model = Product
    form_class = ProductForm
    template_name = "staff/forms/product_form.html"
    slug_url_kwarg = "slug"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Updated successfully! 👍")
        return response

    def get_success_url(self):
        return reverse_lazy("product_detail",
                            kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = self.object
        return context


class CoffeeUpdateView(ProductUpdateView):
    """
    View for updating existing Coffee Products
    """
    model = Coffee
    form_class = CoffeeForm


class ProductCreateView(StaffMemberRequiredMixin, CreateView):
    """
    View for creating new Products
    """
    model = Product
    form_class = ProductForm
    template_name = "staff/forms/product_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, f"{self.object.name} added successfully! 👍")
        return response

    def get_success_url(self):
        return reverse_lazy("product_detail",
                            kwargs={"slug": self.object.slug})


class CoffeeCreateView(ProductCreateView):
    """
    View for creating new Coffee Products
    """
    model = Coffee
    form_class = CoffeeForm
    template_name = "staff/forms/product_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_coffee"] = True
        return context

    def get_success_url(self):
        return reverse_lazy("product_detail",
                            kwargs={"slug": self.object.slug})


class ProductDeleteView(StaffMemberRequiredMixin, DeleteView):
    """
    View for confirmation page to delete a product (or coffee)
    """
    model = Product
    template_name = "staff/forms/product_delete_form.html"
    success_url = reverse_lazy("products")

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(
            request, f"{self.object.name} has been deleted successfully!")
        return response


# Views related to Departments:


class DepartmentCreateView(StaffMemberRequiredMixin, CreateView):
    """
    View for creating new Departments
    """
    model = Department
    form_class = DepartmentForm
    template_name = "staff/forms/department_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Department added successfully! 👍")
        return response

    def get_success_url(self):
        return reverse_lazy("manage_shop")


class DepartmentUpdateView(StaffMemberRequiredMixin, UpdateView):
    """
    View for updating existing Departments
    """
    model = Department
    form_class = DepartmentForm
    template_name = "staff/forms/department_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Updated successfully! 👍")
        return response

    def get_success_url(self):
        return reverse_lazy("manage_shop")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["department"] = self.object
        return context


class DepartmentDeleteView(StaffMemberRequiredMixin, DeleteView):
    """
    View for confirmation page to delete a department.
    """
    model = Department
    template_name = "staff/forms/department_delete_form.html"
    success_url = reverse_lazy("manage_shop")

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(
            request, f"{self.object.name} has been deleted successfully!")
        return response


# Views related to Categories:


class CategoryCreateView(StaffMemberRequiredMixin, CreateView):
    """
    View for creating new Categories
    """
    model = Category
    form_class = CategoryForm
    template_name = "staff/forms/category_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Category added successfully! 👍")
        return response

    def get_success_url(self):
        return reverse_lazy("manage_shop")


class CategoryUpdateView(StaffMemberRequiredMixin, UpdateView):
    """
    View for updating existing Categories
    """
    model = Category
    form_class = CategoryForm
    template_name = "staff/forms/category_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Updated successfully! 👍")
        return response

    def get_success_url(self):
        return reverse_lazy("manage_shop")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.object
        return context


class CategoryDeleteView(StaffMemberRequiredMixin, DeleteView):
    """
    View for confirmation page to delete a category.
    """
    model = Category
    template_name = "staff/forms/category_delete_form.html"
    success_url = reverse_lazy("manage_shop")

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(
            request, f"{self.object.name} has been deleted successfully!")
        return response


class BrandCreateView(StaffMemberRequiredMixin, CreateView):
    """
    View for creating new Brands
    """
    model = Brand
    fields = ["name", "display_name"]
    template_name = "staff/forms/brand_form.html"

    def get_form_action(self):
        return reverse("brand_create")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        helper = FormHelper()
        helper.form_method = "post"
        helper.form_action = self.get_form_action()
        helper.add_input(Submit("submit", "Update", css_class="btn, btn-cc"))
        form.helper = helper
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Brand added successfully! 👍")
        return response

    def get_success_url(self):
        return reverse_lazy("manage_shop")


class BrandUpdateView(StaffMemberRequiredMixin, UpdateView):
    """
    View for updating existing Brands
    """
    model = Brand
    fields = ["name", "display_name", "description"]
    template_name = "staff/forms/brand_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Updated successfully! 👍")
        return response

    def get_form_action(self):
        return reverse("brand_update",  kwargs={"pk": self.object.id})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        helper = FormHelper()
        helper.form_method = "post"
        helper.form_action = self.get_form_action()
        helper.add_input(Submit("submit", "Update", css_class="btn, btn-cc"))
        form.helper = helper
        return form

    def get_success_url(self):
        return reverse_lazy("manage_shop")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.object
        return context


class BrandDeleteView(StaffMemberRequiredMixin, DeleteView):
    """
    View for confirmation page to delete a category.
    """
    model = Brand
    template_name = "staff/forms/brand_delete_form.html"
    success_url = reverse_lazy("manage_shop")

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(
            request, f"{self.object.name} has been deleted successfully!")
        return response


class ManageProductsView(StaffMemberRequiredMixin, ListView):
    """
    renders view for all products, including sorting and searching
    """
    model = Product
    template_name = "staff/manage_products.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()

        wishlist = self.kwargs.get("wishlist")
        department = self.kwargs.get("department")
        category = self.kwargs.get("category")
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
        elif sort == "stock":
            if order == "asc":
                queryset = queryset.order_by("stock")
            else:
                queryset = queryset.order_by("-stock")
        elif sort == "lifetime_sales":
            if order == "asc":
                queryset = queryset.order_by("lifetime_sales")
            else:
                queryset = queryset.order_by("-lifetime_sales")
        elif sort == "visible_to_customers":
            if order == "asc":
                queryset = queryset.order_by("visible_to_customers")
            else:
                queryset = queryset.order_by("-visible_to_customers")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        department = self.kwargs.get("department")
        category = self.kwargs.get("category")

        sort = self.request.GET.get("sort")
        order = self.request.GET.get("order")

        page_number = self.request.GET.get("page")

        # Add the current sorting order as a query
        # parameter to pagination links
        if page_number:
            pagination_links = context["paginator"].get_elided_page_range(
                number=page_number, on_each_side=2)
            pagination_links = [
                f'{reverse("manage_products")}?{self.request.GET.urlencode()}&page={i}' for i in pagination_links]  # noqa
        else:
            pagination_links = context["paginator"].get_elided_page_range(
                on_each_side=2)
            pagination_links = [
                f'{reverse("manage_products")}?{self.request.GET.urlencode()}&page={i}' for i in pagination_links]  # noqa

        context["pagination_links"] = pagination_links

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
        elif sort == "visible_to_customers":
            if order == "asc":
                context["sort_selected"] = "Hidden First"
            else:
                context["sort_selected"] = "On Display First"

        context["category"] = get_object_or_404(
            Category, name=category) if category else None

        context["department"] = get_object_or_404(
            Department, name=department) if department else None

        return context


# Orders


class OrderDispatchView(StaffMemberRequiredMixin, View):
    """
    View for showing setting an order as dispatched,
    redirects to the Order Detail View
    """

    def get(self, request, *args, **kwargs):
        order_number = self.kwargs.get("order_number")
        order = get_object_or_404(Order, order_number=order_number)
        try:
            order.set_as_shipped()
            send_dispatch_email(order)
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


# Purge Stale Guest Carts

class PurgeStaleCartsView(StaffMemberRequiredMixin, FormView):
    """
    View for page to allow staff to purge stale guest carts from the db
    """
    template_name = "staff/forms/purge_stale_guest_carts.html"
    form_class = PurgeStaleCartsForm
    success_url = reverse_lazy("manage_shop")

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        self.purge_carts()

        return super().form_valid(form)

    def get_stale_carts(self):
        """
        Get carts associated with Guests updated more than 2 weeks ago
        """
        return Cart.objects.filter(
            guest_id__isnull=False,
            updated__lt=timezone.now()-timezone.timedelta(weeks=2))

    def purge_carts(self):
        """
        Deletes the stale carts from DB
        """
        stale_carts = self.get_stale_carts()
        stale_carts_num = stale_carts.count()
        # Delete Stale Carts from DB
        stale_carts.delete()

        messages.success(self.request,
                         f"{stale_carts_num} stale carts have been deleted.")
        return stale_carts_num

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stale_carts_count'] = self.get_stale_carts().count()
        return context
