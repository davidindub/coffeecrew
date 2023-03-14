from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from products.models import Product, Coffee, Department, Category


class ProductForm(forms.ModelForm):
    """
    Form for adding or editing non-Coffee products
    """
    class Meta:
        model = Product
        fields = ["name", "visible_to_customers", "description", "brand",
                  "category", "price", "stock", "image"]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(
            Submit("submit", "Save", css_class="btn btn-cc"))


class CoffeeForm(ProductForm):
    """
    Form for adding or editing Coffee products
    """
    class Meta:
        model = Coffee
        fields = ["name", "visible_to_customers", "description", "brand",
                  "category", "stock", "image",
                  "country", "process", "harvest_year", "weight"]


class DepartmentForm(forms.ModelForm):
    """
    Form for adding or editing Departments
    """
    class Meta:
        model = Department
        fields = ["name", "description", "visible_to_customers"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(
            Submit("submit", "Save", css_class="btn btn-cc"))


class CategoryForm(forms.ModelForm):
    """
    Form for adding or editing Categories
    """
    class Meta:
        model = Category
        fields = ["name", "display_name", "description", "department"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(
            Submit("submit", "Save", css_class="btn btn-cc"))


class PurgeStaleCartsForm(forms.Form):
    """
    Form for purging stale guest carts
    """
    purge_stale_carts = forms.BooleanField(
        required=True,
        label="Are you sure you want to purge these carts?"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(
            Submit("submit", "Purge Cards", css_class="btn btn-cc"))
