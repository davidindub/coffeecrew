from products.models import Product, Coffee, Department, Category
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ProductForm(forms.ModelForm):
    """
    Form for adding or editing non-Coffee products
    """
    class Meta:
        model = Product
        fields = ["name", "description", "brand",
                  "category", "price", "stock", "image"]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(
            Submit("submit", "Save", css_class="custom-button"))


class CoffeeForm(ProductForm):
    """
    Form for adding or editing Coffee products
    """
    class Meta:
        model = Coffee
        fields = ["name", "description", "brand", "category", "stock", "image",
                  "country", "process", "harvest_year", "weight"]


class DepartmentForm(forms.ModelForm):
    """
    Form for adding or editing Departments
    """
    class Meta:
        model = Department
        fields = ["name", "visible_to_customers"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(
            Submit("submit", "Save", css_class="custom-button"))


class CategoryForm(forms.ModelForm):
    """
    Form for adding or editing Categories
    """
    class Meta:
        model = Category
        fields = ["name", "display_name", "department"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(
            Submit("submit", "Save", css_class="custom-button"))
