from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField


class ContactForm(forms.Form):
    """
    Form for the contact us page
    """
    full_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={
        "placeholder": "Enter your message here",
        "rows": 5,
        "required": True,
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            FloatingField(
                "full_name",
                "email",
                "message"
            ),
            Submit("submit", "Send", css_class="btn btn-cc"),
        )
