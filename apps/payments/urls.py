# payments/urls.py
from django.urls import path
from .views import (
    buy_antique,
    checkout_result,
    OrderDetailView,
    OrderListView,
    stripe_webhook,
)
from .views.test_webhook import test_order_creation

app_name = 'payments'

urlpatterns = [
    path('buy/<slug:slug>/', buy_antique, name='buy_antique'),
    path('webhook/', stripe_webhook, name='stripe_webhook'),
    path('checkout/<str:status>/', checkout_result, name='checkout_result'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/<uuid:order_id>/', OrderDetailView.as_view(), name='order_detail'),
    # DEBUG ONLY - Remove in production
    path('test-order/<slug:antique_slug>/', test_order_creation, name='test_order_creation'),
]
