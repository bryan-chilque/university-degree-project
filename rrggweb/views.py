from django import shortcuts, urls
from django.contrib.auth import views as views_auth
from django.views.generic import CreateView, FormView, ListView, TemplateView

import rrgg.models

from . import forms
from .utils import SeguroItem


class LoginView(views_auth.LoginView):
    template_name = "rrggweb/login.html"

    def form_valid(self, form):
        consultant_id = (
            form.get_user().consultant_membership.first().consultant.id
        )
        self.next_page = urls.reverse(
            "rrggweb:home", kwargs={"consultant_id": consultant_id}
        )
        return super().form_valid(form)


# HOME
class HomeView(TemplateView):
    template_name = "rrggweb/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seguros"] = [
            SeguroItem(
                "Seguro de vehicular",
                urls.reverse(
                    "rrggweb:quotation:insurance:vehicle:list",
                    kwargs={"consultant_id": self.kwargs["consultant_id"]},
                ),
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

    model = rrgg.models.QuotationInsuranceVehicle
    fields = ["insurance_vehicle_price", "observations"]

    def form_valid(self, form):
        form.instance.consultant_id = self.kwargs["consultant_id"]
        form.instance.customer_id = self.kwargs["customer_id"]
        form.instance.vehicle_id = self.kwargs["vehicle_id"]
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["consultant"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["consultant_id"]
        )
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.Customer, id=self.kwargs["customer_id"]
        )
        context["vehicle"] = shortcuts.get_object_or_404(
            rrgg.models.Vehicle, id=self.kwargs["vehicle_id"]
        )
        return context

    def get_success_url(self):
        return urls.reverse_lazy(
            "rrggweb:quotation:insurance:vehicle:list",
            kwargs={"consultant_id": self.kwargs["consultant_id"]},
        )


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
                kwargs={
                    "consultant_id": self.kwargs["consultant_id"],
                    "customer_id": customer.id,
                },
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
                "consultant_id": self.kwargs["consultant_id"],
                "customer_id": self.kwargs["customer_id"],
                "vehicle_id": self.object.id,
            },
        )


class QuotationInsuranceVehicleCreateCustomerView(CreateView):
    template_name = "rrggweb/quotation/insurance/vehicle/create_customer.html"
    model = rrgg.models.Customer
    fields = [
        "document_number",
        "first_name",
        "last_name",
        "email",
        "phone_number",
    ]

    # TODO: Validar que el documento no exista y agregar lógica
