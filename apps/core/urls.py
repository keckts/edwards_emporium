from django.urls import include, path

from .views import (
        IndexView,
        DashboardView,
        AboutView,
        TermsOfServiceView,
        PrivacyPolicyView,
        )

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("about/", AboutView.as_view(), name="about"),
    path("terms-of-service/", TermsOfServiceView.as_view(), name="terms-of-service"),
    path("privacy-policy/", PrivacyPolicyView.as_view(), name="privacy-policy"),
]
