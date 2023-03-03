from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django_countries.fields import CountryField


class CheckoutAddressForm(forms.Form):
    full_name = forms.CharField(max_length=200, label="Full Name")
    address_line_1 = forms.CharField(max_length=200, label="Address Line 1")
    address_line_2 = forms.CharField(max_length=200, label="Address Line 2")
    city = forms.CharField(max_length=200, label="City")
    postcode = forms.CharField(max_length=200, label="Postcode")
    country = CountryField().formfield()

    def __init__(self, *args, **kwargs):
        super(CheckoutAddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_action = "{% url 'checkout_payment' %}"
        self.helper.add_input(
            Submit("submit", "Save and Continue to Payment",
                   css_class="btn-cc"))
