import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView

from apps.antiques.models import Antique
from ..models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def buy_antique(request, slug):
    antique = get_object_or_404(Antique, slug=slug)
    quantity = int(request.POST.get('quantity', 1))

    try:
        # Create Stripe Checkout Session directly here to avoid circular import
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': antique.title},
                    'unit_amount': int(antique.price * 100),
                },
                'quantity': quantity,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('payments:checkout_result', args=['success'])),
            cancel_url=request.build_absolute_uri(reverse('payments:checkout_result', args=['cancel'])),
            customer_email=request.user.email,  # Prefill customer email
            metadata={
                'user_id': str(request.user.id),
                'antique_id': str(antique.id),
                'quantity': quantity,
            },
        )
        return redirect(session.url)
    except stripe.error.StripeError as e:
        messages.error(request, f"Payment could not be processed: {e.user_message if hasattr(e, 'user_message') else str(e)}")
        return redirect('antiques:antique-detail', slug=antique.slug)

def checkout_result(request, status):
    if status not in ('success', 'cancel'):
        raise Http404("Invalid checkout status")
    return render(request, 'payments/checkout_result.html', {'status': status})

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'payments/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at').prefetch_related('orderitem_set__antique__images')

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'payments/order_detail.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

