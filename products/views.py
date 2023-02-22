from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.views import generic, View
from django.contrib import messages
from .models import Product, Coffee, Category, Department
from profiles.models import WishList
from .forms import ProductForm, CoffeeForm, DepartmentForm
from django.urls import reverse_lazy


class ProductsList(generic.ListView):
    """
    renders view for all products, including sorting and searching
    """
    model = Product
    template_name = "products/products.html"
    context_object_name = "products"

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()

        wishlist = self.kwargs.get('wishlist')
        department = self.kwargs.get('department')
        category = self.kwargs.get('category')
        query = self.request.GET.get('search', None)

        sort = self.request.GET.get('sort')
        order = self.request.GET.get('order')

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

        wishlist = self.kwargs.get('wishlist')
        department = self.kwargs.get('department')
        category = self.kwargs.get('category')
        query = self.request.GET.get('search', None)

        sort = self.request.GET.get('sort')
        order = self.request.GET.get('order')

        if sort == 'name':
            if order == 'asc':
                context["sort_selected"] = "Name (A-Z)"
            else:
                context["sort_selected"] = "Name (Z-A)"
        elif sort == 'price':
            if order == 'asc':
                context["sort_selected"] = "Price (Low to High)"
            else:
                context["sort_selected"] = "Price (High to Low)"
        elif sort == 'date_added':
            context["sort_selected"] = "Newest First"

        context["category"] = get_object_or_404(
            Category, name=category) if category else None

        context["department"] = get_object_or_404(
            Department, name=department) if department else None

        if wishlist:
            context["wishlist_page"] = True

        return context


def product_detail(request, slug):
    """
    View for an single products full details
    """
    product = get_object_or_404(Product, slug=slug)

    context = {"product": product}
    return render(request, "products/product_detail.html", context)


class StaffMemberRequiredMixin(UserPassesTestMixin):
    """
    Check is the user a staff member to restrict access
    """
    def test_func(self):
        return self.request.user.is_staff


class ProductUpdate(StaffMemberRequiredMixin, generic.edit.UpdateView):
    """
    View for updating existing Products
    """
    model = Product
    form_class = ProductForm
    template_name = "products/forms/product_form.html"
    slug_url_kwarg = "slug"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Updated successfully! 👍")
        return response

    def get_success_url(self):
        return reverse_lazy("product_detail",
                            kwargs={"product_id": self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = self.object
        return context


class CoffeeUpdate(ProductUpdate):
    model = Coffee
    form_class = CoffeeForm


class ProductCreate(StaffMemberRequiredMixin, generic.edit.CreateView):
    """
    View for creating new Products
    """
    model = Product
    form_class = ProductForm
    template_name = "products/forms/product_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Product added successfully! 👍")
        return response

    def get_success_url(self):
        return reverse_lazy("product_detail",
                            kwargs={"product_id": self.object.id})


class DepartmentCreate(StaffMemberRequiredMixin, generic.edit.CreateView):
    """
    View for creating new Departments
    """
    model = Department
    form_class = DepartmentForm
    template_name = "products/forms/department_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Department added successfully! 👍")
        return response

    def get_success_url(self):
        return reverse_lazy("category_list_staff")


class DepartmentUpdate(StaffMemberRequiredMixin, generic.edit.UpdateView):
    """
    View for updating existing Departments
    """
    model = Department
    form_class = DepartmentForm
    template_name = "products/forms/department_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Updated successfully! 👍")
        return response

    def get_success_url(self):
        return reverse_lazy("category_list_staff")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["department"] = self.object
        return context


class DepartmentDelete(StaffMemberRequiredMixin, generic.DeleteView):
    """
    View for confirmation page to delete a department.
    """
    model = Department
    template_name = "products/forms/department_delete_form.html"
    success_url = reverse_lazy("category_list_staff")

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.success(
            request, f"{self.object.name} has been deleted successfully!")
        return response


class ManageCategories(generic.ListView):
    """
    View for management dash
    """
    template_name = 'products/staff/manage_categories.html'
    queryset = Department.objects.all()
    context_object_name = 'departments'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        departments = context['departments']
        for department in departments:
            department.categories = Category.objects.filter(
                department=department).order_by('name')
        return context
