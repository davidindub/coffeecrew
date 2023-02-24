from .models import Profile
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ProfileForm(forms.ModelForm):
    """
    Form for editing user profiles
    """
    class Meta:
        model = Profile
        fields = ["default_phone_number"]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(
            Submit("submit", "Save", css_class="btn-cc"))