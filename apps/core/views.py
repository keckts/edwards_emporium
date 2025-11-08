from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import RedirectView, TemplateView


class IndexView(RedirectView):
    """
    Homepage view.
    Redirects authenticated users to their dashboard, redirects non-authenticated users to the index page.
    """

    pattern_name = "dashboard"

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().get_redirect_url(*args, **kwargs)
        return None

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)
        return render(request, "core/index.html")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"
    login_url = reverse_lazy("index")  # Redirect to index if not logged in
