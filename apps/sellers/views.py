from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
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

class SellerUpdateView(SuccessMessageMixin, UpdateView):
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
        return Seller.objects.select_related('user')

class SellerDashboardView(TemplateView):
    template_name = "sellers/seller_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seller'] = get_object_or_404(Seller, user=self.request.user)
        return context

class SellerConfirmationView(TemplateView):
    template_name = "sellers/seller_confirmation.html"
