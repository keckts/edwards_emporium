from django.db import models
from django.conf import settings
from django.utils.text import slugify
from apps.antiques.models import Base

STATUS_CHOICES = (
    ("draft", "Draft"),
    ("published", "Published"),
)


class BlogPost(Base):
    # Core Fields
    content = models.TextField(blank=True, null=True)  # HTML field for rich text

    # New Fields for Control and SEO
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="draft"
    )  # Draft/Published
    slug = models.SlugField(
        max_length=250, unique=True, blank=True
    )  # URL-friendly title (auto-generated from title if not set)

    topic = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="blog_images/", blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-generate slug from title if not provided"""
        if not self.slug and self.title:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            # Ensure unique slug
            while BlogPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("blog:blogpost-detail", kwargs={"slug": self.slug})

    def get_reading_time(self):
        """Calculate reading time based on content"""
        if not self.content:
            return 1
        word_count = len(self.content.split())
        reading_time_minutes = max(
            1, word_count // 200
        )  # Assuming average reading speed of 200 wpm
        return reading_time_minutes
