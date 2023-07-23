from django import shortcuts, urls
from django.contrib.auth import views as views_auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
    View,
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
class QuotationInsuranceVehicleReportXlsxView(View):
    def get(self, request, *args, **kwargs):
        quotation = shortcuts.get_object_or_404(
            rrgg.models.QuotationInsuranceVehicle,
            id=kwargs["quotation_id"],
        )

        workbook = self.create_workbook(quotation)

        response = HttpResponse(
            content_type="application/vnd.openxmlformats"
            + "-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = (
            "attachment; filename=report_quotations.xlsx"
        )

        workbook.save(response)
        return response

    def create_workbook(self, quotation):
        from openpyxl import load_workbook

        wb = load_workbook(filename="rrggweb/resources/report_quotations.xlsx")

        ws = wb.active
        ws["C11"] = quotation.insured_amount
        ws["I6"] = quotation.created.strftime("%d/%m/%Y")

        vehicle = quotation.vehicle
        ws["C7"] = vehicle.brand
        ws["C8"] = vehicle.vehicle_model
        ws["C9"] = vehicle.fabrication_year
        ws["C10"] = vehicle.use_type.name

        customer = vehicle.customer
        ws["C6"] = f"{customer.given_name} {customer.first_surname}"

        for premium in quotation.premiums.all():
            ratio = premium.insurance_vehicle_ratio
            insurance_vehicle = ratio.insurance_vehicle
            if premium.amount > 0 and insurance_vehicle.id == 1:
                ws["E13"] = premium.amount
                ws["E14"] = ws["E13"].value * ratio.emission_right
                ws["E15"] = (ws["E13"].value + ws["E14"].value) * ratio.tax
                ws["E16"] = ws["E13"].value + ws["E14"].value + ws["E15"].value
            if premium.amount > 0 and insurance_vehicle.id == 2:
                ws["G13"] = premium.amount
                ws["G14"] = ws["G13"].value * ratio.emission_right
                ws["G15"] = (ws["G13"].value + ws["G14"].value) * ratio.tax
                ws["G16"] = ws["G13"].value + ws["G14"].value + ws["G15"].value
            if premium.amount > 0 and insurance_vehicle.id == 3:
                ws["I13"] = premium.amount
                ws["I14"] = ws["I13"].value * ratio.emission_right
                ws["I15"] = (ws["I13"].value + ws["I14"].value) * ratio.tax
                ws["I16"] = ws["I13"].value + ws["I14"].value + ws["I15"].value
            if premium.amount > 0 and insurance_vehicle.id == 4:
                ws["K13"] = premium.amount
                ws["K14"] = ws["K13"].value * ratio.emission_right
                ws["K15"] = (ws["K13"].value + ws["K14"].value) * ratio.tax
                ws["K16"] = ws["K13"].value + ws["K14"].value + ws["K15"].value
            if premium.amount > 0 and insurance_vehicle.id == 5:
                ws["M13"] = premium.amount
                ws["M14"] = ws["M13"].value * ratio.emission_right
                ws["M15"] = (ws["M13"].value + ws["M14"].value) * ratio.tax
                ws["M16"] = ws["M13"].value + ws["M14"].value + ws["M15"].value

        return wb


class QuotationInsuranceVehicleListView(ListView):
    template_name = "rrggweb/quotation/insurance/vehicle/list.html"
    model = rrgg.models.QuotationInsuranceVehicle


class QuotationInsuranceVehicleInsuredAmountCreateView(
    rrgg_mixins.RrggBootstrapDisplayMixin, CreateView
):
    template_name = "rrggweb/quotation/insurance/vehicle/create_quotation.html"

    model = rrgg.models.QuotationInsuranceVehicle
    fields = ["insured_amount"]

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
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:create_premiums",
            kwargs={
                "consultant_id": self.kwargs["consultant_id"],
                "customer_id": self.kwargs["customer_id"],
                "vehicle_id": self.kwargs["vehicle_id"],
                "quotation_id": self.object.id,
            },
        )


# QUOTATION INSURANCE VEHICLE PREMIUM


class QuotationInsuranceVehicleDetailView(DetailView):
    template_name = "rrggweb/quotation/insurance/vehicle/detail.html"
    model = rrgg.models.QuotationInsuranceVehicle
    pk_url_kwarg = "quotation_id"


class QuotationInsuranceVehiclePremiumsFormView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/create_premiums.html"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["queryset"] = rrgg.models.InsuranceVehicle.objects.none()
        return kwargs

    def get_form(self):
        form_class = modelformset_factory(
            rrgg.models.QuotationInsuranceVehiclePremium,
            extra=rrgg.models.InsuranceVehicle.objects.count(),
            fields="__all__",
        )
        formset = super().get_form(form_class)
        # Mantener el orden: Ver ABC123
        insurance_vehicles = rrgg.models.InsuranceVehicle.objects.order_by(
            "name"
        )
        for form, insurance_vehicle in zip(formset, insurance_vehicles):
            insurance_vehicle_ratio = form.fields["insurance_vehicle_ratio"]
            quotation_insurance_vehicle = form.fields[
                "quotation_insurance_vehicle"
            ]

            insurance_vehicle_ratio.initial = insurance_vehicle.last_ratio
            quotation_insurance_vehicle.initial = shortcuts.get_object_or_404(
                rrgg.models.QuotationInsuranceVehicle,
                id=self.kwargs["quotation_id"],
            )

            insurance_vehicle_ratio.widget = forms.forms.HiddenInput()
            quotation_insurance_vehicle.widget = forms.forms.HiddenInput()

        return formset

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
        context["quotation"] = shortcuts.get_object_or_404(
            rrgg.models.QuotationInsuranceVehicle,
            id=self.kwargs["quotation_id"],
        )

        # Mantener el orden: Ver ABC123
        insurance_vehicles = rrgg.models.InsuranceVehicle.objects.order_by(
            "name"
        )
        last_ratios = (
            insurance_vehicle.last_ratio
            for insurance_vehicle in insurance_vehicles
        )
        context["last_ratio_forms"] = zip(last_ratios, context["form"])

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
            "rrggweb:quotation:insurance:vehicle:insured_amount",
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
