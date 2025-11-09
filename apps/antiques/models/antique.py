import random
import uuid

from django.conf import settings
from django.db import models
from django.db.models import Max
from django.utils.text import slugify
from apps.sellers.models import Seller
from .base import Base


class Antique(Base):
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_sold = models.BooleanField(default=False)
    type_of_antique = models.CharField(max_length=100)

    slug = models.SlugField(max_length=255, unique=True, blank=True)

    dimensions = models.CharField(max_length=100, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    additional_info = models.TextField(blank=True)

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="antiques", null=True)
    stripe_product_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return f"/antiques/{self.slug}/"

    def save(self, *args, **kwargs):
        # Generate slug if missing
        if not self.slug:
            base_slug = slugify(self.title)
            unique_id = str(uuid.uuid4())[:8]
            self.slug = f"{base_slug}-{unique_id}"
            # Note: unique id has 16^8 = 4,294,967,296 combinations, low collision risk

        # Auto-update sold status
        self.is_sold = self.quantity == 0

        super().save(*args, **kwargs)

    def get_primary_image(self):
        return self.images.first()


class AntiqueImage(models.Model):
    antique = models.ForeignKey(
        Antique,
        on_delete=models.CASCADE,  # delete images if antique is deleted
        related_name="images",
    )
    image = models.ImageField(upload_to="antiques/")

    def __str__(self):
        return f"Image for {self.antique.title} ({self.id})"
