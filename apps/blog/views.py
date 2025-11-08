from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from braces.views import SuperuserRequiredMixin
from apps.core.mixins import BaseModelViewMixin, SearchableListViewMixin

from .forms import BlogPostForm
from .models import BlogPost


class BlogPostListView(SearchableListViewMixin, ListView):
    model = BlogPost
    template_name = "blog/blogpost_list.html"
    context_object_name = "object_list"
    paginate_by = 12

    # SearchableListViewMixin configuration
    search_fields = ["title__icontains", "content__icontains", "topic__icontains"]
    filter_fields = {"status": "status", "topic": "topic"}
    default_ordering = ["-created_at"]

    def get_queryset(self):
        """Only show published posts to non-superusers."""
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(status="published")
        return queryset

    def get_filter_context(self):
        """Provide filter options for the template."""
        return {
            "topic_options": (
                BlogPost.objects.values_list("topic", flat=True)
                .distinct()
                .order_by("topic")
            ),
            "status_options": ["draft", "published"]
            if self.request.user.is_superuser
            else [],
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "page_title": "Blog",
                "page_subtitle": "Insights, stories, and updates from our collection",
                "show_filters": True,
                "search_placeholder": "Search blog posts...",
                "object_count": self.object_list.count() if self.object_list else 0,
                "object_name": "blog post",
                "empty_message": "No blog posts found matching your criteria.",
            }
        )

        # Add filter fields for search_filter.html partial
        filter_fields = []

        # Topic filter
        topics = list(context["topic_options"])
        if topics:
            filter_fields.append(
                {
                    "name": "topic",
                    "label": "Topic",
                    "type": "select",
                    "options": topics,
                    "current": self.request.GET.get("topic", ""),
                }
            )

        # Status filter (for superusers only)
        if self.request.user.is_superuser:
            filter_fields.append(
                {
                    "name": "status",
                    "label": "Status",
                    "type": "select",
                    "options": context["status_options"],
                    "current": self.request.GET.get("status", ""),
                }
            )

        context["filter_fields"] = filter_fields

        # Add create button for superusers
        if self.request.user.is_superuser:
            context["create_url"] = reverse_lazy("blog:blogpost-create")
            context["create_button_text"] = "New Post"

        return context


class BlogPostDetailView(DetailView, BaseModelViewMixin):
    model = BlogPost
    action = "detail"

    def get_object(self, queryset=None):
        obj = BlogPost.objects.get(slug=self.kwargs["slug"])
        # Only allow viewing drafts for superusers
        if obj.status == "draft" and not self.request.user.is_superuser:
            raise PermissionDenied("This blog post is not published yet.")
        return obj


class BlogPostCreateView(SuperuserRequiredMixin, CreateView, BaseModelViewMixin):
    model = BlogPost
    form_class = BlogPostForm
    action = "form"

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to create blog posts.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_title': 'Create New Blog Post',
            'form_description': 'Share insights, stories, and updates with your audience',
            'submit_text': 'Publish Post',
            'cancel_url': reverse_lazy('blog:blogpost-list'),
            'back_url': reverse_lazy('blog:blogpost-list'),
            'back_text': 'Back to Blog',
        })
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, f"Blog post '{self.object.title}' created successfully!"
        )
        return response


class BlogPostUpdateView(UpdateView, BaseModelViewMixin, UserPassesTestMixin):
    model = BlogPost
    form_class = BlogPostForm
    action = "form"

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to edit blog posts.")

    def get_object(self, queryset=None):
        return BlogPost.objects.get(slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_title': f'Edit Blog Post',
            'form_description': f'Update "{self.object.title}"',
            'submit_text': 'Update Post',
            'cancel_url': self.object.get_absolute_url(),
            'back_url': reverse_lazy('blog:blogpost-list'),
            'back_text': 'Back to Blog',
        })
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, f"Blog post '{self.object.title}' updated successfully!"
        )
        return response


class BlogPostDeleteView(DeleteView, BaseModelViewMixin, UserPassesTestMixin):
    model = BlogPost
    action = "confirm_delete"
    success_url = reverse_lazy("blog:blogpost-list")

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to delete blog posts.")

    def get_object(self, queryset=None):
        return BlogPost.objects.get(slug=self.kwargs["slug"])

    def delete(self, request, *args, **kwargs):
        blogpost = self.get_object()
        blogpost_title = blogpost.title
        messages.success(request, f"Blog post '{blogpost_title}' deleted successfully!")
        return super().delete(request, *args, **kwargs)


@method_decorator(csrf_exempt, name="dispatch")
class BlogImageUploadView(SuperuserRequiredMixin, View):
    """Handle image uploads for Quill editor"""

    def post(self, request):
        if "image" not in request.FILES:
            return JsonResponse({"error": "No image provided"}, status=400)

        image = request.FILES["image"]

        # Validate file type
        if not image.content_type.startswith("image/"):
            return JsonResponse({"error": "File must be an image"}, status=400)

        # Save the image
        file_path = f"blog_content_images/{image.name}"
        saved_path = default_storage.save(file_path, image)
        image_url = default_storage.url(saved_path)

        return JsonResponse({"url": image_url})
