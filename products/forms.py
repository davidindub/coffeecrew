from products.models import Product, Coffee
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "brand", "category", "stock", "image"]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save"))
