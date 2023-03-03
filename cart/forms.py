from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("full_name", "email", "address_line_1", "address_line_2",
                  "city", "postcode", "country")

    def __init__(self, *args, **kwargs):
        """
        """
    super().__init__(*args, **kwargs)
    # placeholders = {}

    self.fields["full_name"].widget.attrs["autofocus"] = True
