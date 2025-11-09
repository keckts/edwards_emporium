import logging
import stripe
import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from apps.antiques.models import Antique
from ..models import Order, OrderItem

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY
User = get_user_model()


@csrf_exempt
def stripe_webhook(request):
    logger.info("=" * 80)
    logger.info("WEBHOOK RECEIVED - Starting processing")
    logger.info("=" * 80)

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', None)

    logger.debug(f"Signature header present: {bool(sig_header)}")
    logger.debug(f"Endpoint secret configured: {bool(endpoint_secret)}")

    # Handle webhook signature verification
    if endpoint_secret and sig_header:
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
            logger.info("✓ Webhook signature verified successfully")
        except (ValueError, stripe.error.SignatureVerificationError) as e:
            logger.warning(f"✗ Webhook signature verification failed: {e}")
            return HttpResponse(status=400)
    else:
        # Development mode - parse JSON directly without verification
        import json
        logger.warning("⚠️ DEVELOPMENT MODE: Processing webhook without signature verification")
        try:
            event = json.loads(payload)
        except json.JSONDecodeError as e:
            logger.error(f"✗ Invalid JSON payload: {e}")
            return HttpResponse(status=400)

    event_type = event.get("type", "unknown")
    logger.info(f"Event Type: {event_type}")

    # Handle checkout session completion
    if event_type == "checkout.session.completed":
        logger.info(">>> Processing checkout.session.completed event")
        session = event["data"]["object"]
        session_id = session.get("id", "unknown")
        logger.info(f"Session ID: {session_id}")

        metadata = session.get("metadata", {})
        logger.debug(f"Metadata received: {metadata}")

        user_id = metadata.get("user_id")
        antique_id = metadata.get("antique_id")
        quantity = int(metadata.get("quantity", 1))

        logger.info(f"Extracted - user_id: {user_id}, antique_id: {antique_id}, quantity: {quantity}")

        if not user_id or not antique_id:
            logger.error("✗ Missing user_id or antique_id in session metadata")
            return HttpResponse(status=400)

        try:
            # Try to get user by ID first
            user = None
            if user_id:
                try:
                    logger.debug(f"Looking up user with id: {user_id}")
                    user = User.objects.get(id=int(user_id))
                    logger.info(f"✓ Found user by ID: {user.username} (ID: {user.id})")
                except (User.DoesNotExist, ValueError):
                    logger.warning(f"User not found with id: {user_id}")

            # Fallback: try to get user from session customer email
            if not user:
                customer_email = session.get("customer_details", {}).get("email") or session.get("customer_email")
                if customer_email:
                    logger.debug(f"Trying to find user by email: {customer_email}")
                    try:
                        user = User.objects.get(email=customer_email)
                        logger.info(f"✓ Found user by email: {user.username} ({customer_email})")
                    except User.DoesNotExist:
                        logger.error(f"✗ No user found with email: {customer_email}")
                        return HttpResponse(status=404)
                else:
                    logger.error("✗ No user_id in metadata and no customer email in session")
                    return HttpResponse(status=400)

            # Antique model uses UUID IDs
            logger.debug(f"Parsing antique UUID: {antique_id}")
            try:
                antique_uuid = uuid.UUID(antique_id)
                logger.debug(f"✓ UUID parsed successfully: {antique_uuid}")
            except (ValueError, AttributeError) as e:
                logger.error(f"✗ Invalid antique_id format: {antique_id} - {e}")
                return HttpResponse(status=400)

            logger.debug(f"Looking up antique with UUID: {antique_uuid}")
            antique = Antique.objects.get(id=antique_uuid)
            logger.info(f"✓ Found antique: {antique.title} (Current quantity: {antique.quantity})")

            logger.info(f"Creating order for {user.username} - {antique.title}")

            with transaction.atomic():
                logger.debug("Creating Order object...")
                order = Order.objects.create(
                    user=user,
                    stripe_session_id=session["id"],
                    status="paid"
                )
                logger.info(f"✓ Order created with ID: {order.id}")

                logger.debug("Creating OrderItem...")
                OrderItem.objects.create(order=order, antique=antique, quantity=quantity)
                logger.info(f"✓ OrderItem created (quantity: {quantity})")

                # Update antique quantity
                old_quantity = antique.quantity
                antique.quantity = max(0, antique.quantity - quantity)
                antique.save()
                logger.info(f"✓ Antique quantity updated: {old_quantity} → {antique.quantity}")

            logger.info("=" * 80)
            logger.info(f"SUCCESS: Order {order.id} completed!")
            logger.info(f"  User: {user.username}")
            logger.info(f"  Antique: {antique.title}")
            logger.info(f"  Quantity: {quantity}")
            logger.info(f"  Stock: {old_quantity} → {antique.quantity}")
            logger.info("=" * 80)

        except User.DoesNotExist:
            logger.error(f"✗ User not found with id: {user_id}")
            return HttpResponse(status=404)
        except Antique.DoesNotExist:
            logger.error(f"✗ Antique not found with id: {antique_id}")
            return HttpResponse(status=404)
        except Exception as e:
            logger.exception(f"✗ EXCEPTION while creating order: {e}")
            return HttpResponse(status=500)

    # Handle invoice events
    elif event_type in ["invoice.finalized", "invoice.payment_succeeded"]:
        logger.info(f">>> Processing {event_type} event")
        invoice = event["data"]["object"]
        invoice_id = invoice.get("id", "unknown")
        logger.info(f"Invoice ID: {invoice_id}")

        payment_intent_id = invoice.get("payment_intent")
        order = None

        if payment_intent_id:
            try:
                order = Order.objects.filter(stripe_payment_intent=payment_intent_id).first()
                if order:
                    logger.info(f"✓ Found order for payment intent: {order.id}")
            except Exception as e:
                logger.error(f"✗ Error finding order for payment intent: {e}")

        if order and invoice.get("invoice_pdf"):
            order.stripe_invoice_pdf = invoice["invoice_pdf"]
            order.save()
            logger.info(f"✓ Invoice PDF saved for order {order.id}")
        elif not order:
            logger.warning("Could not find associated order for invoice")
    else:
        logger.info(f"Ignoring event type: {event_type}")

    logger.info("Webhook processing complete - returning 200 OK")
    return HttpResponse(status=200)


def create_stripe_session(request, user, antique, quantity=1):
    """
    Helper function to create a Stripe checkout session.
    You could extend this to other objects in the future.
    """

    return stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'aud',
                'product_data': {'name': antique.title},
                'unit_amount': int(antique.price * 100),
            },
            'quantity': quantity,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payments:checkout_result', args=['success'])),
        cancel_url=request.build_absolute_uri(reverse('payments:checkout_result', args=['cancel'])),
        metadata={
            'user_id': str(user.id),
            'antique_id': str(antique.id),
            'quantity': quantity,
        },
    )
