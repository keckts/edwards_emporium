from django.urls import path

from .views import (
    BlogImageUploadView,
    BlogPostCreateView,
    BlogPostDeleteView,
    BlogPostDetailView,
    BlogPostListView,
    BlogPostUpdateView,
)

app_name = "blog"

urlpatterns = [
    path("", BlogPostListView.as_view(), name="blogpost-list"),
    path("create/", BlogPostCreateView.as_view(), name="blogpost-create"),
    path("upload-image/", BlogImageUploadView.as_view(), name="upload-image"),
    path("<slug:slug>/", BlogPostDetailView.as_view(), name="blogpost-detail"),
    path("<slug:slug>/edit/", BlogPostUpdateView.as_view(), name="blogpost-update"),
    path(
        "<slug:slug>/delete/", BlogPostDeleteView.as_view(), name="blogpost-delete"
    ),
]
