from django.urls import path
from .views import (
    SellerCreateView,
    SellerUpdateView,
    SellerDetailView,
    SellerDashboardView,
    SellerConfirmationView,
        )

app_name = 'sellers'

urlpatterns = [
    path("create/", SellerCreateView.as_view(), name="seller-create"),
    path("update/<uuid:pk>/", SellerUpdateView.as_view(), name="seller-update"),
    path("detail/<uuid:pk>/", SellerDetailView.as_view(), name="seller-detail"),
    path("dashboard/", SellerDashboardView.as_view(), name="seller-dashboard"),
    path("confirmation/", SellerConfirmationView.as_view(), name="seller-confirmation"),
]
