import random

from django.conf import settings
from django.db import models
from django.db.models import Max
from django.utils.text import slugify

from .base import Base


class Antique(Base):
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_sold = models.BooleanField(default=False)
    type_of_antique = models.CharField(max_length=100)

    slug = models.SlugField(max_length=255, unique=True, blank=True)
    short_id = models.PositiveIntegerField(
        unique=True, editable=False, null=True, blank=True
    )

    dimensions = models.CharField(max_length=100, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    additional_info = models.TextField(blank=True)

    stripe_product_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["short_id"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.short_id})"

    def get_absolute_url(self):
        return f"/antiques/{self.short_id}-{self.slug}/"

    def save(self, *args, **kwargs):
        # Efficient short_id generation — no random guessing
        if not self.short_id:
            max_id = Antique.objects.aggregate(max_id=Max("short_id"))["max_id"] or 9999
            self.short_id = max_id + 1

        # Generate slug if missing
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Antique.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

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
