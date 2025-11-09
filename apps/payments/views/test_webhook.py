"""
Test view to manually trigger webhook logic for debugging.
ONLY USE IN DEVELOPMENT - Remove in production!
"""
import logging
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from apps.antiques.models import Antique
from apps.users.models import User
from ..models import Order, OrderItem

logger = logging.getLogger(__name__)


@staff_member_required
def test_order_creation(request, antique_slug):
    """
    Manual test endpoint to create an order without Stripe.
    Visit: /payments/test-order/<antique-slug>/
    """
    try:
        antique = get_object_or_404(Antique, slug=antique_slug)
        user = request.user
        quantity = 1

        logger.info(f"TEST: Creating order for {user.username} - {antique.title}")

        # Create order
        order = Order.objects.create(
            user=user,
            stripe_session_id=f"test_{antique.id}",
            status="paid"
        )
        logger.info(f"TEST: Order created with ID: {order.id}")

        # Create order item
        OrderItem.objects.create(
            order=order,
            antique=antique,
            quantity=quantity
        )
        logger.info(f"TEST: OrderItem created")

        # Update stock
        old_quantity = antique.quantity
        antique.quantity = max(0, antique.quantity - quantity)
        antique.save()
        logger.info(f"TEST: Stock updated {old_quantity} → {antique.quantity}")

        return JsonResponse({
            'success': True,
            'order_id': str(order.id),
            'antique': antique.title,
            'user': user.username,
            'old_stock': old_quantity,
            'new_stock': antique.quantity,
        })

    except Exception as e:
        logger.exception(f"TEST: Error creating order: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
