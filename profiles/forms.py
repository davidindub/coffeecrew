from .models import Profile, Address
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class UpdateEmailForm(forms.Form):
    email = forms.EmailField(label='New Email')


class ProfileForm(forms.ModelForm):
    """
    For for updating user profiles
    """

    class Meta:
        model = Profile
        fields = ["default_phone_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save"))


class AddressForm(forms.ModelForm):
    """
    Form for editing user addresses
    """
    class Meta:
        model = Address
        fields = ["address_line_1", "address_line_2",
                  "city", "postcode", "country"]

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(
            Submit("submit", "Save", css_class="btn-cc"))
