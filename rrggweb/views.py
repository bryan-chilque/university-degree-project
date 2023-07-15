from django import shortcuts, urls
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
    fields = ["insurance_vehicle_price", "observations"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.Customer, id=self.kwargs["customer_id"]
        )
        context["vehicle"] = shortcuts.get_object_or_404(
            rrgg.models.Vehicle, id=self.kwargs["vehicle_id"]
        )
        return context


class QuotationInsuranceVehicleSearchView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/search.html"
    form_class = forms.SearchByDocumentNumberForm

    def form_valid(self, form):
        document_number = form.cleaned_data["document_number"]
        customer_exists = rrgg.models.Customer.objects.filter(
            document_number=document_number
        ).exists()
        if customer_exists:
            customer = rrgg.models.Customer.objects.get(
                document_number=document_number
            )
            self.success_url = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:create_vehicle",
                kwargs={"customer_id": customer.id},
            )
        else:
            self.success_url = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:create_customer"
            )
        return super().form_valid(form)


class QuotationInsuranceVehicleCreateVehicleView(CreateView):
    template_name = "rrggweb/quotation/insurance/vehicle/create_vehicle.html"
    model = rrgg.models.Vehicle
    fields = ["brand", "vehicle_model", "property_number", "fabrication_year"]

    def form_valid(self, form):
        form.instance.customer_id = self.kwargs["customer_id"]
        return super().form_valid(form)

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:create",
            kwargs={
                "customer_id": self.kwargs["customer_id"],
                "vehicle_id": self.object.id,
            },
        )
