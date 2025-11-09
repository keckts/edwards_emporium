from django import forms
from django.forms import inlineformset_factory

from .models import Antique, AntiqueImage, Wishlist


class AntiqueForm(forms.ModelForm):
    """Form for creating or editing an Antique object."""

    class Meta:
        model = Antique
        exclude = {
            "id",
            "user",
            "created_at",
            "slug",
            "updated_at",
            "is_sold",
            "seller",
            "stripe_product_id",
            "stripe_price_id",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add DaisyUI classes to form fields
        self.fields["title"].widget.attrs.update(
            {
                "class": "input input-bordered w-full",
                "placeholder": "e.g., Rare Victorian Teapot",
            }
        )
        self.fields["description"].widget.attrs.update(
            {
                "class": "textarea textarea-bordered w-full",
                "rows": 3,
                "placeholder": "Brief description (shows in listings)",
            }
        )
        self.fields["content"].widget.attrs.update(
            {
                "class": "textarea textarea-bordered w-full",
                "rows": 5,
                "placeholder": "Detailed content about the antique",
            }
        )
        self.fields["price"].widget.attrs.update(
            {
                "class": "input input-bordered w-full",
                "step": "0.01",
                "placeholder": "Enter price",
            }
        )
        self.fields["type_of_antique"].widget.attrs.update(
            {
                "class": "input input-bordered w-full",
                "placeholder": "e.g., Furniture, Jewelry, Art",
            }
        )
        self.fields["dimensions"].widget.attrs.update(
            {
                "class": "input input-bordered w-full",
                "placeholder": "e.g., Height 32cm x Width 20cm x Depth 15cm",
            }
        )
        self.fields["quantity"].widget.attrs.update(
            {"class": "input input-bordered w-full", "min": "1", "step": "1"}
        )
        self.fields["additional_info"].widget.attrs.update(
            {
                "class": "textarea textarea-bordered w-full",
                "rows": 3,
                "placeholder": "Any additional information",
            }
        )


class AntiqueImageForm(forms.ModelForm):
    """Form for uploading an image related to an Antique."""

    class Meta:
        model = AntiqueImage
        fields = ["image"]
        widgets = {
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "file-input file-input-bordered w-full",
                    "accept": "image/*",
                }
            ),
        }


# ✅ Use inlineformset_factory instead of modelformset_factory
AntiqueImageFormSet = inlineformset_factory(
    parent_model=Antique,
    model=AntiqueImage,
    form=AntiqueImageForm,
    fields=["image"],
    extra=3,  # Display three empty image fields by default
    max_num=10,  # Maximum 10 images
    can_delete=True,
)


class WishlistForm(forms.ModelForm):
    """Form for creating or editing a Wishlist object."""

    class Meta:
        model = Wishlist
        fields = ["title"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update(
            {
                "class": "input input-bordered w-full",
                "placeholder": "e.g., My Favorite Antiques",
            }
        )
