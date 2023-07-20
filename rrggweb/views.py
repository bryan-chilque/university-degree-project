from django import shortcuts, urls
from django.contrib.auth import views as views_auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

import rrgg.models
from rrgg import mixins as rrgg_mixins

from . import forms
from .utils import SeguroItem

# LOGIN


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


# LOGOUT


class LogoutView(views_auth.LogoutView):
    next_page = urls.reverse_lazy("rrggweb:login")


# HOME


class HomeView(TemplateView):
    template_name = "rrggweb/home.html"


# QUOTATION VIEW


class QuotationView(TemplateView):
    template_name = "rrggweb/quotation.html"

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


class QuotationInsuranceVehicleCreateView(
    rrgg_mixins.RrggBootstrapDisplayMixin, CreateView
):
    template_name = "rrggweb/quotation/insurance/vehicle/create_quotation.html"

    model = rrgg.models.QuotationInsuranceVehicle
    fields = ["insurance_vehicle_price", "amount_insured", "observations"]

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


# QUOTATION INSURANCE VEHICLE PREMIUM GENERATION


class QuotationInsuranceVehiclePremiumGenerationView(ListView):
    template_name = (
        "rrggweb/quotation/insurance/vehicle/premium_generation.html"
    )
    model = rrgg.models.InsuranceVehicle


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
            create_customer_url = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:create_customer",
                kwargs={"consultant_id": self.kwargs["consultant_id"]},
            )
            self.success_url = (
                f"{create_customer_url}?document_number={document_number}"
            )
        return super().form_valid(form)


class QuotationInsuranceVehicleCreateVehicleView(
    rrgg_mixins.RrggBootstrapDisplayMixin, CreateView
):
    template_name = "rrggweb/quotation/insurance/vehicle/create_vehicle.html"
    model = rrgg.models.Vehicle
    fields = [
        "brand",
        "vehicle_model",
        "plate",
        "fabrication_year",
        "engine",
        "chassis",
        "use_type",
    ]

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["consultant"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["consultant_id"]
        )
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.Customer, id=self.kwargs["customer_id"]
        )
        return context


class QuotationInsuranceVehicleUpdateVehicleView(
    rrgg_mixins.RrggBootstrapDisplayMixin, UpdateView
):
    template_name = "rrggweb/quotation/insurance/vehicle/update_vehicle.html"
    model = rrgg.models.Vehicle
    fields = "__all__"
    pk_url_kwarg = "vehicle_id"

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:create",
            kwargs={
                "consultant_id": self.kwargs["consultant_id"],
                "customer_id": self.object.customer.id,
                "vehicle_id": self.object.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["consultant"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["consultant_id"]
        )
        return context


class QuotationInsuranceVehicleCreateCustomerView(
    LoginRequiredMixin, rrgg_mixins.RrggBootstrapDisplayMixin, CreateView
):
    template_name = "rrggweb/quotation/insurance/vehicle/create_customer.html"
    model = rrgg.models.Customer
    fields = "__all__"

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:create_vehicle",
            kwargs={
                "consultant_id": self.kwargs["consultant_id"],
                "customer_id": self.object.id,
            },
        )

    def get_initial(self):
        initial = super().get_initial()
        initial["document_number"] = self.request.GET.get(
            "document_number", ""
        )
        return initial


class QuotationInsuranceVehicleUpdateCustomerView(
    rrgg_mixins.RrggBootstrapDisplayMixin, UpdateView
):
    template_name = "rrggweb/quotation/insurance/vehicle/update_customer.html"
    model = rrgg.models.Customer
    fields = "__all__"
    pk_url_kwarg = "customer_id"

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:create_vehicle",
            kwargs={
                "consultant_id": self.kwargs["consultant_id"],
                "customer_id": self.object.id,
            },
        )
