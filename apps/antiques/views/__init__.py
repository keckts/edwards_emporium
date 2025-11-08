"""
Antiques app views.

This module organizes views into separate files:
- antique_views: CRUD operations for Antique model
- wishlist_views: Wishlist functionality with HTMX support
"""

from .antique_views import (AntiqueCreateView, AntiqueDeleteView,
                            AntiqueDetailView, AntiqueListView,
                            AntiqueUpdateView)
from .wishlist_views import (WishlistCreateView, WishlistDeleteView,
                             WishlistDetailView, WishlistListView,
                             WishlistToggleView,
                             wishlist_add_antique, wishlist_remove_antique)

__all__ = [
    # Antique views
    "AntiqueListView",
    "AntiqueDetailView",
    "AntiqueCreateView",
    "AntiqueUpdateView",
    "AntiqueDeleteView",
    # Wishlist views
    "WishlistListView",
    "WishlistDetailView",
    "WishlistCreateView",
    "WishlistDeleteView",
    "WishlistToggleView",
    "wishlist_add_antique",
    "wishlist_remove_antique",
]
