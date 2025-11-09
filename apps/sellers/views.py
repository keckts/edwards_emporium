from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Avg, Count, Q
from .models import Seller
from .forms import SellerForm
from django.urls import reverse_lazy

class SellerCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Seller
    form_class = SellerForm
    template_name = "sellers/seller_form.html"
    success_url = reverse_lazy('sellers:seller-confirmation')
    success_message = "Seller profile created successfully. Welcome to Edward's Emporium!"

    def form_valid(self, form):
        # automatically assign the new user
        form.instance.user = self.request.user
        return super().form_valid(form)

class SellerUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Seller
    form_class = SellerForm
    template_name = "sellers/seller_form.html"
    success_url = reverse_lazy('sellers:seller-dashboard')
    success_message = "Seller profile updated successfully."

    def get_object(self, queryset=None):
        # Ensure that only the owner can update their profile
        return Seller.objects.get(user=self.request.user)

class SellerDetailView(DetailView): # this page is mostly for users looking at the seller
    model = Seller
    template_name = "sellers/seller_detail.html"

    def get_queryset(self):
        return Seller.objects.select_related('user').prefetch_related('antiques')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all antiques from this seller
        context['antiques'] = self.object.antiques.all().order_by('-created_at')
        return context

class SellerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "sellers/seller_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seller = get_object_or_404(Seller, user=self.request.user)
        context['seller'] = seller

        # Get all antiques for this seller
        antiques = seller.antiques.all()

        # Calculate statistics
        context['total_antiques'] = antiques.count()
        context['active_antiques'] = antiques.filter(is_sold=False).count()
        context['sold_antiques'] = antiques.filter(is_sold=True).count()

        # Calculate revenue from sold items
        total_revenue = antiques.filter(is_sold=True).aggregate(
            total=Sum('price')
        )['total'] or 0
        context['total_revenue'] = total_revenue

        # Calculate average price
        avg_price = antiques.aggregate(avg=Avg('price'))['avg'] or 0
        context['avg_price'] = avg_price

        # Calculate sold percentage
        if context['total_antiques'] > 0:
            context['sold_percentage'] = int((context['sold_antiques'] / context['total_antiques']) * 100)
        else:
            context['sold_percentage'] = 0

        # Get recent antiques (last 5)
        context['recent_antiques'] = antiques.select_related().prefetch_related('images').order_by('-created_at')[:5]

        return context

class SellerConfirmationView(LoginRequiredMixin, TemplateView):
    template_name = "sellers/seller_confirmation.html"
