from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid


class Seller(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="seller"
    )

    # Store information
    store_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    # Contact & address
    email = models.EmailField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    notes = models.TextField(
        blank=True, null=True
    )  # this is just notes from seller for user to see
    address = models.TextField(blank=True, null=True)

    # Seller status & metrics
    is_verified = models.BooleanField(default=False)  # if store is verified

    # social media links
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    pinterest = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    # styling
    profile_picture = models.ImageField(
        upload_to="seller_profiles/", blank=True, null=True
    )

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        # create a slug on save based on username
        self.slug = self.user.username.lower().replace(" ", "-")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.store_name} - {self.user.email}"
