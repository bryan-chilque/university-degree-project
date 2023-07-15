from django import urls
from django.contrib.auth import views as views_auth
from django.views.generic import CreateView, FormView, ListView, TemplateView

import rrgg.models

from . import forms
from .utils import SeguroItem


class LoginView(views_auth.LoginView):
    template_name = "rrggweb/login.html"
    next_page = urls.reverse_lazy("rrggweb:home")


# HOME
class HomeView(TemplateView):
    template_name = "rrggweb/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seguros"] = [
            SeguroItem(
                "Seguro de vehicular",
                urls.reverse("rrggweb:quotation:insurance:vehicle:list"),
            ),
            SeguroItem("Seguro de vida", ""),
            SeguroItem("Seguro de accidentes", ""),
            SeguroItem("Seguro de salud", ""),
        ]
        return context


# QUOTATION INSURANCE VEHICLE
class QuotationInsuranceVehicleListView(ListView):
    template_name = "rrggweb/quotation/insurance/vehicle/list.html"
    model = rrgg.models.QuotationInsuranceVehicle


class QuotationInsuranceVehicleCreateView(CreateView):
    template_name = "rrggweb/quotation/insurance/vehicle/create.html"
    success_url = urls.reverse_lazy("rrggweb:quotation:insurance:vehicle:list")
    model = rrgg.models.QuotationInsuranceVehicle
    fields = "__all__"


class QuotationInsuranceVehicleSearchView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/search.html"
    form_class = forms.SearchByDocumentNumberForm

    def form_valid(self, form):
        document_number = form.cleaned_data["document_number"]
        customer_exists = rrgg.models.Customer.objects.filter(
            document_number=document_number
        ).exists()
        if customer_exists:
            self.success_url = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:create_vehicle"
            )
        else:
            self.success_url = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:create_customer"
            )
        return super().form_valid(form)
