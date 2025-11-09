from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.core.mixins import (
    BaseModelViewMixin,
    SearchableListViewMixin,
    VerifiedSellerRequiredMixin,
)
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from ..forms import AntiqueForm, AntiqueImageFormSet
from ..models import Antique, AntiqueImage, Wishlist


class AntiqueListView(SearchableListViewMixin, ListView):
    model = Antique
    template_name = "antiques/antique_list.html"
    paginate_by = 20

    # SearchableListViewMixin configuration
    search_fields = [
        "title__icontains",
        "description__icontains",
        "type_of_antique__icontains",
    ]
    prefetch_related_fields = ["images"]
    default_ordering = ["-created_at"]

    def get_queryset(self):
        """Apply custom sold filter."""
        queryset = super().get_queryset()

        # Type filter
        antique_type = self.request.GET.get("type", "").strip()
        if antique_type:
            queryset = queryset.filter(type_of_antique=antique_type)

        # Sold filter (hide sold items by default)
        show_sold = self.request.GET.get("show_sold", "")
        if show_sold != "true":
            queryset = queryset.filter(is_sold=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all unique antique types for the filter dropdown
        context["antique_types"] = (
            Antique.objects.values_list("type_of_antique", flat=True)
            .distinct()
            .order_by("type_of_antique")
        )

        # Safely get user's wishlist (returns the first if multiple exist)
        if self.request.user.is_authenticated:
            context["wishlist"] = Wishlist.objects.filter(
                user=self.request.user
            ).first()
        else:
            context["wishlist"] = None

        return context


class AntiqueDetailView(DetailView, BaseModelViewMixin):
    model = Antique
    action = "detail"

    def get_object(self, queryset=None):
        return Antique.objects.get(slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add wishlist status for authenticated users
        if self.request.user.is_authenticated:
            context['in_wishlist'] = Wishlist.objects.filter(
                user=self.request.user,
                antiques=self.object
            ).exists()
        else:
            context['in_wishlist'] = False

        return context


class AntiqueCreateView(VerifiedSellerRequiredMixin, CreateView, BaseModelViewMixin):
    model = Antique
    form_class = AntiqueForm
    action = "form"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["image_formset"] = AntiqueImageFormSet(
                self.request.POST, self.request.FILES
            )
        else:
            context["image_formset"] = AntiqueImageFormSet(
                queryset=AntiqueImage.objects.none()
            )
        context.update({
            'form_title': 'Add New Antique',
            'form_description': 'Fill in the details to add a new antique to your collection',
            'submit_text': 'Create Antique',
            'cancel_url': reverse_lazy('antiques:antique-list'),
            'back_url': reverse_lazy('antiques:antique-list'),
            'back_text': 'Back to Antiques',
        })
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context["image_formset"]
        form.instance.user = self.request.user
        form.instance.seller = self.request.user.seller

        with transaction.atomic():
            self.object = form.save()

            if image_formset.is_valid():
                image_formset.instance = self.object
                images = image_formset.save(commit=False)

                # Limit to 10 images
                if len(images) + self.object.images.count() > 10:
                    messages.error(
                        self.request, "Maximum 10 images allowed per antique."
                    )
                    return self.form_invalid(form)

                for image in images:
                    image.antique = self.object
                    image.save()

                # Handle deletions
                for obj in image_formset.deleted_objects:
                    obj.delete()

                messages.success(
                    self.request, f"Antique '{self.object.title}' created successfully!"
                )
                return redirect(self.object.get_absolute_url())
            else:
                return self.form_invalid(form)


class AntiqueUpdateView(VerifiedSellerRequiredMixin, UpdateView, BaseModelViewMixin):
    model = Antique
    form_class = AntiqueForm
    action = "form"

    def get_object(self, queryset=None):
        return Antique.objects.get(slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["image_formset"] = AntiqueImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            context["image_formset"] = AntiqueImageFormSet(instance=self.object)
        context.update({
            'form_title': 'Edit Antique',
            'form_description': f'Update the details for "{self.object.title}"',
            'submit_text': 'Update Antique',
            'cancel_url': self.object.get_absolute_url(),
            'back_url': reverse_lazy('antiques:antique-list'),
            'back_text': 'Back to Antiques',
        })
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context["image_formset"]

        with transaction.atomic():
            self.object = form.save()

            if image_formset.is_valid():
                images = image_formset.save(commit=False)

                # Count new images being added
                new_images_count = len([img for img in images if not img.pk])
                existing_count = self.object.images.count()

                # Limit to 10 images
                if new_images_count + existing_count > 10:
                    messages.error(
                        self.request,
                        f"Maximum 10 images allowed. You have {existing_count} and are trying to add {new_images_count} more.",
                    )
                    return self.form_invalid(form)

                for image in images:
                    image.antique = self.object
                    image.save()

                # Handle deletions
                for obj in image_formset.deleted_objects:
                    obj.delete()

                messages.success(
                    self.request, f"Antique '{self.object.title}' updated successfully!"
                )
                return redirect(self.object.get_absolute_url())
            else:
                return self.form_invalid(form)


class AntiqueDeleteView(VerifiedSellerRequiredMixin, DeleteView, BaseModelViewMixin):
    model = Antique
    action = "confirm_delete"
    success_url = reverse_lazy("antiques:antique-list")

    def get_object(self, queryset=None):
        return Antique.objects.get(slug=self.kwargs["slug"])

    def get(self, request, *args, **kwargs):
        """Handle GET request - return modal for HTMX or full page"""
        antique = self.get_object()

        # If HTMX request, return just the modal
        if request.headers.get("HX-Request"):
            warning_parts = ["This antique will be permanently deleted."]
            if antique.images.exists():
                warning_parts.append(
                    f"{antique.images.count} associated image{'s' if antique.images.count > 1 else ''} will also be deleted."
                )

            context = {
                "object": antique,
                "item_type": "antique",
                "modal_title": "Delete Antique?",
                "warning_message": " ".join(warning_parts),
                "delete_url": reverse_lazy(
                    "antiques:antique-delete",
                    kwargs={"slug": antique.slug},
                ),
            }
            return render(request, "antiques/partials/delete_modal.html", context)

        # Otherwise return full confirmation page
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Handle antique deletion"""
        antique = self.get_object()
        antique_title = antique.title

        messages.success(request, f"Antique '{antique_title}' deleted successfully!")
        return super().delete(request, *args, **kwargs)
