from django.db import models

from .antique import Antique
from .base import Base


class Wishlist(Base):
    antiques = models.ManyToManyField(Antique, related_name="wishlists", blank=True)

    def __str__(self):
        return f"{self.title}"
