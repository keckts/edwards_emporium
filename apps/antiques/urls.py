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
    # Wishlist URLs
    path("wishlist/", WishlistListView.as_view(), name="wishlist-list"),
    path(
        "wishlist/toggle/<uuid:antique_id>/",
        WishlistToggleView.as_view(),
        name="wishlist-toggle",
    ),
    path(
        "wishlist/<uuid:pk>/add/<uuid:antique_id>/",
        wishlist_add_antique,
        name="wishlist-add-antique",
    ),
    path(
        "wishlist/<uuid:pk>/remove/<uuid:antique_id>/",
        wishlist_remove_antique,
        name="wishlist-remove-antique",
    ),
    path("wishlist/create/", WishlistCreateView.as_view(), name="wishlist-create"),
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
]
