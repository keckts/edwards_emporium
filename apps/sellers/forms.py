# sellers/forms.py
from django import forms
from django.forms import Textarea
from phonenumber_field.formfields import PhoneNumberField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit
from .models import Seller

class SellerForm(forms.ModelForm):
    phone_number = PhoneNumberField(required=False)

    class Meta:
        model = Seller
        fields = [
            "store_name",
            "description",
            "email",
            "phone_number",
            "notes",
            "address",
            "facebook",
            "instagram",
            "twitter",
            "pinterest",
            "linkedin",
            "website",
        ]
        widgets = {
            "description": Textarea(attrs={"rows": 3}),
            "notes": Textarea(attrs={"rows": 2}),
            "address": Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Crispy Forms helper
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Field("store_name"),
            Field("description"),
            Div(
                Field("email"),
                Field("phone_number"),
                Field("address"),
            ),
            Field("notes"),
            Div(
                Field("facebook"),
                Field("instagram"),
                Field("twitter"),
                Field("pinterest"),
                Field("linkedin"),
                Field("website"),
            ),
            Submit("submit", "Save Seller")
        )
