from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.contrib.messages.views import SuccessMessageMixin
from apps.core.mixins import BaseModelViewMixin

from ..forms import WishlistForm
from ..models import Antique, Wishlist


class WishlistListView(LoginRequiredMixin, ListView):
    template_name = "antiques/wishlists/wishlist_list.html"
    paginate_by = 10

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).order_by("-created_at")


class WishlistDetailView(DetailView, BaseModelViewMixin):
    model = Wishlist
    action = "detail"
    template_name = "antiques/wishlists/wishlist_detail.html"

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


class WishlistCreateView(SuccessMessageMixin, CreateView, BaseModelViewMixin):
    model = Wishlist
    action = "form"
    form_class = WishlistForm
    template_name = "antiques/wishlists/wishlist_form.html"
    success_url = reverse_lazy("antiques:wishlist-list")
    success_message = "Wishlist '%(title)s' created successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_title': 'Create Wishlist',
            'form_description': 'Create a new wishlist to organize your favorite antiques',
            'submit_text': 'Create Wishlist',
            'cancel_url': reverse_lazy('antiques:wishlist-list'),
            'back_url': reverse_lazy('antiques:wishlist-list'),
        })
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class WishlistUpdateView(SuccessMessageMixin, UpdateView, BaseModelViewMixin):
    model = Wishlist
    action = "form"
    form_class = WishlistForm
    template_name = "antiques/wishlists/wishlist_form.html"
    success_url = reverse_lazy("antiques:wishlist-list")
    success_message = "Wishlist '%(title)s' updated successfully!"

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_title': f'Edit Wishlist',
            'form_description': 'Update the name of your wishlist',
            'submit_text': 'Update Wishlist',
            'cancel_url': reverse_lazy('antiques:wishlist-list'),
            'back_url': reverse_lazy('antiques:wishlist-list'),
        })
        return context


class WishlistDeleteView(LoginRequiredMixin, DeleteView):
    model = Wishlist
    template_name = "antiques/wishlists/wishlist_confirm_delete.html"
    success_url = reverse_lazy("antiques:wishlist-list")

    def get_queryset(self):
        """Ensure users can only delete their own wishlists"""
        return Wishlist.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        """Handle GET request - return modal for HTMX or full page"""
        wishlist = self.get_object()

        # If HTMX request, return just the modal
        if request.headers.get("HX-Request"):
            context = {
                "object": wishlist,
                "item_type": "wishlist",
                "modal_title": "Delete Wishlist?",
                "warning_message": "Deleting this wishlist will permanently remove it. The antiques themselves will not be deleted.",
                "delete_url": reverse_lazy(
                    "antiques:wishlist-delete", kwargs={"pk": wishlist.pk}
                ),
            }
            return render(request, "antiques/partials/delete_modal.html", context)

        # Otherwise return full confirmation page
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Handle wishlist deletion"""
        wishlist = self.get_object()
        wishlist_title = wishlist.title

        messages.success(request, f"Wishlist '{wishlist_title}' deleted successfully!")
        return super().delete(request, *args, **kwargs)


class WishlistToggleView(LoginRequiredMixin, View):
    """
    HTMX view to toggle antique in wishlists.
    Shows a modal with all user's wishlists when clicked.
    """

    def get(self, request, antique_id):
        """Show modal with wishlist selection"""
        antique = get_object_or_404(Antique, id=antique_id)
        user_wishlists = Wishlist.objects.filter(user=request.user)

        # Get which wishlists currently contain this antique
        wishlist_statuses = []
        for wishlist in user_wishlists:
            wishlist_statuses.append(
                {
                    "wishlist": wishlist,
                    "contains_antique": wishlist.antiques.filter(
                        id=antique_id
                    ).exists(),
                }
            )

        context = {
            "antique": antique,
            "wishlist_statuses": wishlist_statuses,
            "has_wishlists": user_wishlists.exists(),
        }
        return render(request, "antiques/partials/wishlist_modal.html", context)

    def post(self, request, antique_id):
        """Toggle antique in a specific wishlist"""
        antique = get_object_or_404(Antique, id=antique_id)
        wishlist_id = request.POST.get("wishlist_id")

        if wishlist_id:
            wishlist = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)

            # Toggle antique in wishlist
            if wishlist.antiques.filter(id=antique_id).exists():
                wishlist.antiques.remove(antique)
                action = "removed"
                message = f"Removed from {wishlist.title}"
            else:
                wishlist.antiques.add(antique)
                action = "added"
                message = f"Added to {wishlist.title}"

            # Return updated button state
            in_wishlist = Wishlist.objects.filter(
                user=request.user, antiques=antique
            ).exists()

            return render(
                request,
                "antiques/partials/wishlist_button.html",
                {
                    "antique": antique,
                    "in_wishlist": in_wishlist,
                    "message": message,
                },
            )

        return HttpResponse("Invalid request", status=400)


@login_required
def wishlist_add_antique(request, wishlist_id, antique_id):
    """Add an antique to a specific wishlist (HTMX endpoint)"""
    wishlist = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    antique = get_object_or_404(Antique, id=antique_id)

    wishlist.antiques.add(antique)

    # Return updated modal content
    user_wishlists = Wishlist.objects.filter(user=request.user)
    wishlist_statuses = []
    for wl in user_wishlists:
        wishlist_statuses.append(
            {
                "wishlist": wl,
                "contains_antique": wl.antiques.filter(id=antique_id).exists(),
            }
        )

    context = {
        "antique": antique,
        "wishlist_statuses": wishlist_statuses,
        "has_wishlists": user_wishlists.exists(),
        "message": f"Added to {wishlist.title}",
    }
    return render(request, "antiques/partials/wishlist_modal.html", context)


@login_required
def wishlist_remove_antique(request, wishlist_id, antique_id):
    """Remove an antique from a specific wishlist (HTMX endpoint)"""
    wishlist = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    antique = get_object_or_404(Antique, id=antique_id)

    wishlist.antiques.remove(antique)

    # Return updated modal content
    user_wishlists = Wishlist.objects.filter(user=request.user)
    wishlist_statuses = []
    for wl in user_wishlists:
        wishlist_statuses.append(
            {
                "wishlist": wl,
                "contains_antique": wl.antiques.filter(id=antique_id).exists(),
            }
        )

    context = {
        "antique": antique,
        "wishlist_statuses": wishlist_statuses,
        "has_wishlists": user_wishlists.exists(),
        "message": f"Removed from {wishlist.title}",
    }
    return render(request, "antiques/partials/wishlist_modal.html", context)
