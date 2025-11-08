from django.db.models import Q
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied


class SearchableListViewMixin:
    """
    Reusable mixin for ListView with search and filtering capabilities.
    Provides efficient queryset optimization and customizable search fields.
    """

    search_fields = []  # List of fields to search (e.g., ["title__icontains", "description__icontains"])
    filter_fields = {}  # Dict of filter fields with param names (e.g., {"type": "type_of_antique"})
    prefetch_related_fields = []  # List of fields to prefetch
    select_related_fields = []  # List of fields to select_related
    default_ordering = ["-created_at"]  # Default ordering
    paginate_by = 20

    def get_queryset(self):
        """Optimized queryset with search, filters, and efficient loading."""
        queryset = super().get_queryset()

        # Apply select_related and prefetch_related for efficiency
        if self.select_related_fields:
            queryset = queryset.select_related(*self.select_related_fields)
        if self.prefetch_related_fields:
            queryset = queryset.prefetch_related(*self.prefetch_related_fields)

        # Search functionality
        search = self.request.GET.get("search", "").strip()
        if search and self.search_fields:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{field: search})
            queryset = queryset.filter(q_objects)

        # Apply custom filters
        for param_name, field_name in self.filter_fields.items():
            value = self.request.GET.get(param_name, "").strip()
            if value:
                queryset = queryset.filter(**{field_name: value})

        # Apply ordering
        return queryset.order_by(*self.default_ordering)

    def get_filter_context(self):
        """Override this method to add filter-specific context data."""
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_filter_context())
        return context


class BaseModelViewMixin:
    """
    Provides automatic template naming, success URLs, and context names.
    Assumes templates follow the structure: <model_name>s/<model_name>_<action>.html
    Used for CRUD operations.
    """

    model = None  # must be set in subclass
    form_class = None
    context_object_name = None
    action = None  # "detail", "form", etc.

    # Optional overrides
    template_name = None
    success_url = None

    def get_template_names(self):
        """
        Return the template name(s) for this view. If `self.template_name` is set, use it;
        otherwise, generate automatically based on model and action.
        """
        if self.template_name:
            # allow string or list of templates
            return (
                [self.template_name]
                if isinstance(self.template_name, str)
                else self.template_name
            )

        model_name = self.model._meta.model_name
        return [f"{model_name}s/{model_name}_{self.action}.html"]

    def get_context_object_name(self, obj):
        """
        Return context object name for templates.
        """
        return self.context_object_name or self.model._meta.model_name

    def get_success_url(self):
        """
        Return the success URL after form submission. Can be overridden with `self.success_url`.
        """
        if self.success_url:
            # can be a string or a callable
            return (
                self.success_url() if callable(self.success_url) else self.success_url
            )

        # default: reverse_lazy of <model_name>s
        model_name = self.model._meta.model_name
        return reverse_lazy(f"{model_name}s")  # expects a named URL like 'antiques'


class VerifiedSellerRequiredMixin:
    """
    Restrict access to verified sellers who own the Antique instance.
    Works for both object-based (Update/Delete) and non-object (Create) views.
    """

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is a verified seller or superuser
        user = request.user
        if not (
            user.is_superuser or (hasattr(user, "seller") and user.seller.is_verified)
        ):
            raise PermissionDenied("You must be a verified seller to access this page.")

        # For views that involve an existing object, ensure ownership
        if hasattr(self, "get_object"):
            try:
                obj = self.get_object()
            except AttributeError:
                obj = None
            if obj and hasattr(obj, "seller") and obj.seller != user.seller:
                raise PermissionDenied("You do not own this antique.")

        return super().dispatch(request, *args, **kwargs)
