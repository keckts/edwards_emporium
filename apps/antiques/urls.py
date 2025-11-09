from django.urls import path

from .views import (
    AntiqueCreateView,
    AntiqueDeleteView,
    AntiqueDetailView,
    AntiqueListView,
    AntiqueUpdateView,
    WishlistCreateView,
    WishlistDeleteView,
    WishlistDetailView,
    WishlistListView,
    WishlistToggleView,
    wishlist_add_antique,
    wishlist_remove_antique,
)

app_name = "antiques"

urlpatterns = [
    # Antique URLs
    path("", AntiqueListView.as_view(), name="antique-list"),
    path("create/", AntiqueCreateView.as_view(), name="antique-create"),

    # Wishlist URLs (must come before <slug:slug>/ to avoid conflicts)
    path("wishlist/", WishlistListView.as_view(), name="wishlist-list"),
    path("wishlist/create/", WishlistCreateView.as_view(), name="wishlist-create"),
    path(
        "wishlist/toggle/<slug:slug>/",
        WishlistToggleView.as_view(),
        name="wishlist-toggle",
    ),
    path(
        "wishlist/<uuid:pk>/add/<slug:slug>/",
        wishlist_add_antique,
        name="wishlist-add-antique",
    ),
    path(
        "wishlist/<uuid:pk>/remove/<slug:slug>/",
        wishlist_remove_antique,
        name="wishlist-remove-antique",
    ),
    path(
        "wishlist/<uuid:pk>/",
        WishlistDetailView.as_view(),
        name="wishlist-detail",
    ),
    path(
        "wishlist/<uuid:pk>/delete/",
        WishlistDeleteView.as_view(),
        name="wishlist-delete",
    ),

    # Antique detail URLs (must come after wishlist URLs to avoid catching "wishlist" as a slug)
    path(
        "<slug:slug>/",
        AntiqueDetailView.as_view(),
        name="antique-detail",
    ),
    path(
        "<slug:slug>/update/",
        AntiqueUpdateView.as_view(),
        name="antique-update",
    ),
    path(
        "<slug:slug>/delete/",
        AntiqueDeleteView.as_view(),
        name="antique-delete",
    ),
]
