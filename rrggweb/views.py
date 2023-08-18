from django import shortcuts, urls
from django.contrib import messages
from django.contrib.auth import views as views_auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.views.generic import (
    CreateView,
    DeleteView,
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
    form_class = forms.LoginAuthenticationForm

    def form_valid(self, form):
        registrar_id = (
            form.get_user().consultant_membership.first().consultant.id
        )
        self.next_page = urls.reverse(
            "rrggweb:home", kwargs={"registrar_id": registrar_id}
        )
        return super().form_valid(form)


# LOGOUT


class LogoutView(views_auth.LogoutView):
    next_page = urls.reverse_lazy("rrggweb:login")


# HOME


class HomeView(TemplateView):
    template_name = "rrggweb/home.html"


# MENU QUOTATION  VIEW


class QuotationView(TemplateView):
    template_name = "rrggweb/quotation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seguros"] = [
            SeguroItem(
                "Seguro de vehicular",
                urls.reverse(
                    "rrggweb:quotation:insurance:vehicle:list",
                    kwargs={"registrar_id": self.kwargs["registrar_id"]},
                ),
            ),
            SeguroItem("Seguro de vida", ""),
            SeguroItem("Seguro de accidentes", ""),
            SeguroItem("Seguro de salud", ""),
        ]
        return context


# LIST


class QIVListView(ListView):
    template_name = "rrggweb/quotation/insurance/vehicle/list.html"
    model = rrgg.models.QuotationInsuranceVehicle

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(customer__given_name__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_register"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:select_role",
            kwargs={"registrar_id": self.kwargs["registrar_id"]},
        )
        return context


# SELLER


class QIVSelectRoleFormView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/select_role.html"
    form_class = forms.RoleForm

    def form_valid(self, form: forms.RoleForm):
        role = form.cleaned_data["roles"]
        self.success_url = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:select_seller",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "role_id": role.id,
            },
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:list",
            kwargs={"registrar_id": self.kwargs["registrar_id"]},
        )
        return context


class QIVSelectSellerFormView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/select_seller.html"
    form_class = forms.SellerForm

    def form_valid(self, form: forms.SellerForm):
        seller = form.cleaned_data["sellers"]
        self.success_url = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:search_customer",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": seller.id,
            },
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        role_id = self.kwargs.get("role_id")
        kwargs["role_id"] = role_id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:select_role",
            kwargs={"registrar_id": self.kwargs["registrar_id"]},
        )
        return context


# CLIENT


class QIVSearchCustomerView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/search_customer.html"
    form_class = forms.SearchPersonForm

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
                "rrggweb:quotation:insurance:vehicle:search_vehicle",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                    "customer_id": customer.id,
                },
            )
        else:
            create_customer_url = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:create_customer",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                },
            )
            self.success_url = (
                f"{create_customer_url}?document_number={document_number}"
            )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:select_role",
            kwargs={"registrar_id": self.kwargs["registrar_id"]},
        )
        return context


class QIVehicleCreateCustomerView(
    LoginRequiredMixin, rrgg_mixins.RrggBootstrapDisplayMixin, CreateView
):
    template_name = "rrggweb/quotation/insurance/vehicle/create_customer.html"
    model = rrgg.models.Customer
    fields = "__all__"

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:search_vehicle",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.object.id,
            },
        )

    def get_initial(self):
        initial = super().get_initial()
        initial["document_number"] = self.request.GET.get(
            "document_number", ""
        )
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:search_customer",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
            },
        )
        return context


class QIVUpdateCustomerViewSupport(
    rrgg_mixins.RrggBootstrapDisplayMixin, UpdateView
):
    pk_url_kwarg = "customer_id"
    model = rrgg.models.Customer
    fields = "__all__"


class QIVUpdateCustomerStepView(QIVUpdateCustomerViewSupport):
    template_name = (
        "rrggweb/quotation/insurance/vehicle/update_customer_step.html"
    )

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:search_vehicle",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.object.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:search_customer",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
            },
        )
        return context


class QIVUpdateCustomerView(QIVUpdateCustomerViewSupport):
    template_name = "rrggweb/quotation/insurance/vehicle/update_customer.html"

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.kwargs["quotation_id"],
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.kwargs["quotation_id"],
            },
        )
        return context


# VEHICLE


class QIVSearchVehicleView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/search_vehicle.html"
    form_class = forms.SearchVehicleForm

    def form_valid(self, form):
        plate = form.cleaned_data["plate"]
        vehicle_exists = rrgg.models.Vehicle.objects.filter(
            plate=plate
        ).exists()
        if vehicle_exists:
            vehicle = rrgg.models.Vehicle.objects.get(plate=plate)
            vehicle_ownership_exists = (
                rrgg.models.VehicleOwnerShip.objects.filter(
                    vehicle__plate=plate
                ).exists()
            )
            if vehicle_ownership_exists:
                self.success_url = urls.reverse(
                    "rrggweb:quotation:insurance:vehicle:create",
                    kwargs={
                        "registrar_id": self.kwargs["registrar_id"],
                        "seller_id": self.kwargs["seller_id"],
                        "customer_id": self.kwargs["customer_id"],
                        "vehicle_id": vehicle.id,
                    },
                )
            else:
                self.success_url = urls.reverse(
                    "rrggweb:quotation:insurance:vehicle:define_owner",
                    kwargs={
                        "registrar_id": self.kwargs["registrar_id"],
                        "seller_id": self.kwargs["seller_id"],
                        "customer_id": self.kwargs["customer_id"],
                        "vehicle_id": vehicle.id,
                    },
                )
        else:
            create_vehicle_url = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:create_vehicle",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                    "customer_id": self.kwargs["customer_id"],
                },
            )
            self.success_url = f"{create_vehicle_url}?plate={plate}"
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.Customer, id=self.kwargs["customer_id"]
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:update_customer_step",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.kwargs["customer_id"],
            },
        )
        return context


class QIVCreateVehicleView(rrgg_mixins.RrggBootstrapDisplayMixin, CreateView):
    template_name = "rrggweb/quotation/insurance/vehicle/create_vehicle.html"
    model = rrgg.models.Vehicle
    fields = [
        "brand",
        "vehicle_model",
        "plate",
        "fabrication_year",
        "engine",
        "chassis",
        "seat_number",
        "use_type",
        "has_gps",
        "has_endorsee",
        "endorsee_bank",
    ]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["has_gps"].required = False
        form.fields["has_endorsee"].required = False
        form.fields["endorsee_bank"].required = False
        return form

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:define_owner",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.kwargs["customer_id"],
                "vehicle_id": self.object.id,
            },
        )

    def get_initial(self):
        initial = super().get_initial()
        initial["plate"] = self.request.GET.get("plate", "")
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.Customer, id=self.kwargs["customer_id"]
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:search_vehicle",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.kwargs["customer_id"],
            },
        )
        return context


class QIVUpdateVehicleViewSupport(
    rrgg_mixins.RrggBootstrapDisplayMixin, UpdateView
):
    model = rrgg.models.Vehicle
    fields = [
        "brand",
        "vehicle_model",
        "plate",
        "fabrication_year",
        "engine",
        "chassis",
        "seat_number",
        "use_type",
        "has_gps",
        "has_endorsee",
        "endorsee_bank",
    ]
    pk_url_kwarg = "vehicle_id"


class QIVUpdateVehicleStepView(QIVUpdateVehicleViewSupport):
    template_name = (
        "rrggweb/quotation/insurance/vehicle/update_vehicle_step.html"
    )

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:define_owner",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.kwargs["customer_id"],
                "vehicle_id": self.object.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.Customer, id=self.kwargs["customer_id"]
        )
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:update_customer_step",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.kwargs["customer_id"],
            },
        )
        return context


class QIVUpdateVehicleView(QIVUpdateVehicleViewSupport):
    template_name = "rrggweb/quotation/insurance/vehicle/update_vehicle.html"

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.kwargs["quotation_id"],
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.kwargs["quotation_id"],
            },
        )
        return context


# OWNER


class QIVDefineOwnerView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/define_owner.html"
    form_class = forms.DefineOwnerForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["is_owner"].required = False
        return form

    def form_valid(self, form):
        vehicle = shortcuts.get_object_or_404(
            rrgg.models.Vehicle, id=self.kwargs["vehicle_id"]
        )
        vehicle_ownership_exists = rrgg.models.VehicleOwnerShip.objects.filter(
            vehicle=vehicle
        ).exists()
        if vehicle_ownership_exists:
            vehicle.ownership.delete()
        else:
            pass

        is_customer_owner = form.cleaned_data["is_owner"]
        if is_customer_owner:
            customer = shortcuts.get_object_or_404(
                rrgg.models.Customer, id=self.kwargs["customer_id"]
            )
            rrgg.models.VehicleOwnerShip.objects.create(
                customer=customer, vehicle=vehicle
            )
            self.success_url = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:create",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                    "customer_id": self.kwargs["customer_id"],
                    "vehicle_id": self.kwargs["vehicle_id"],
                },
            )
        else:
            self.success_url = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:search_owner",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                    "customer_id": self.kwargs["customer_id"],
                    "vehicle_id": self.kwargs["vehicle_id"],
                },
            )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.Customer, id=self.kwargs["customer_id"]
        )
        context["vehicle"] = shortcuts.get_object_or_404(
            rrgg.models.Vehicle, id=self.kwargs["vehicle_id"]
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:update_vehicle_step",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.kwargs["customer_id"],
                "vehicle_id": self.kwargs["vehicle_id"],
            },
        )
        return context


class QIVSearchOwnerView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/search_owner.html"
    form_class = forms.SearchPersonForm

    def form_valid(self, form):
        document_number = form.cleaned_data["document_number"]
        owner_exists = rrgg.models.Owner.objects.filter(
            document_number=document_number
        ).exists()
        if owner_exists:
            owner = rrgg.models.Owner.objects.get(
                document_number=document_number
            )
            vehicle = shortcuts.get_object_or_404(
                rrgg.models.Vehicle, id=self.kwargs["vehicle_id"]
            )
            rrgg.models.VehicleOwnerShip.objects.create(
                owner=owner, vehicle=vehicle
            )
            self.success_url = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:create",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                    "customer_id": self.kwargs["customer_id"],
                    "vehicle_id": self.kwargs["vehicle_id"],
                },
            )
        else:
            create_owner_url = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:create_owner",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                    "customer_id": self.kwargs["customer_id"],
                    "vehicle_id": self.kwargs["vehicle_id"],
                },
            )
            self.success_url = (
                f"{create_owner_url}?document_number={document_number}"
            )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.Customer, id=self.kwargs["customer_id"]
        )
        context["vehicle"] = shortcuts.get_object_or_404(
            rrgg.models.Vehicle, id=self.kwargs["vehicle_id"]
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:define_owner",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.kwargs["customer_id"],
                "vehicle_id": self.kwargs["vehicle_id"],
            },
        )
        return context


class QIVCreateOwnerView(rrgg_mixins.RrggBootstrapDisplayMixin, CreateView):
    template_name = "rrggweb/quotation/insurance/vehicle/create_owner.html"
    model = rrgg.models.Owner
    fields = "__all__"

    def get_success_url(self):
        vehicle = shortcuts.get_object_or_404(
            rrgg.models.Vehicle, id=self.kwargs["vehicle_id"]
        )
        rrgg.models.VehicleOwnerShip.objects.create(
            owner=self.object, vehicle=vehicle
        )
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:create",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.kwargs["customer_id"],
                "vehicle_id": self.kwargs["vehicle_id"],
            },
        )

    def get_initial(self):
        initial = super().get_initial()
        initial["document_number"] = self.request.GET.get(
            "document_number", ""
        )
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.Customer, id=self.kwargs["customer_id"]
        )
        context["vehicle"] = shortcuts.get_object_or_404(
            rrgg.models.Vehicle, id=self.kwargs["vehicle_id"]
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:search_owner",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.kwargs["customer_id"],
                "vehicle_id": self.kwargs["vehicle_id"],
            },
        )
        return context


class QIVUpdateOwnerViewSupport(
    rrgg_mixins.RrggBootstrapDisplayMixin, UpdateView
):
    model = rrgg.models.Owner
    fields = "__all__"
    pk_url_kwarg = "owner_id"


class QIVUpdateOwnerStepView(QIVUpdateOwnerViewSupport):
    template_name = (
        "rrggweb/quotation/insurance/vehicle/update_owner_step.html"
    )

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:create",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.kwargs["customer_id"],
                "vehicle_id": self.kwargs["vehicle_id"],
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.Customer, id=self.kwargs["customer_id"]
        )
        context["vehicle"] = shortcuts.get_object_or_404(
            rrgg.models.Vehicle, id=self.kwargs["vehicle_id"]
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:define_owner",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.kwargs["customer_id"],
                "vehicle_id": self.kwargs["vehicle_id"],
            },
        )
        return context


class QIVUpdateOwnerView(QIVUpdateOwnerViewSupport):
    template_name = "rrggweb/quotation/insurance/vehicle/update_owner.html"

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.kwargs["quotation_id"],
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.kwargs["quotation_id"],
            },
        )
        return context


# QUOTATION


class QIVCreateView(rrgg_mixins.RrggBootstrapDisplayMixin, CreateView):
    template_name = "rrggweb/quotation/insurance/vehicle/create.html"

    model = rrgg.models.QuotationInsuranceVehicle
    fields = ["insured_amount"]

    def form_valid(self, form):
        form.instance.consultant_registrar_id = self.kwargs["registrar_id"]
        form.instance.consultant_seller_id = self.kwargs["seller_id"]
        form.instance.customer_id = self.kwargs["customer_id"]
        form.instance.vehicle_id = self.kwargs["vehicle_id"]
        return super().form_valid(form)

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:create_premiums",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.object.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.Customer, id=self.kwargs["customer_id"]
        )
        context["vehicle"] = shortcuts.get_object_or_404(
            rrgg.models.Vehicle, id=self.kwargs["vehicle_id"]
        )
        if context["vehicle"].ownership.owner is None:
            context["owner"] = "El cliente es propietario del vehículo."
            context["previous_page"] = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:define_owner",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                    "customer_id": self.kwargs["customer_id"],
                    "vehicle_id": self.kwargs["vehicle_id"],
                },
            )
        else:
            context["owner"] = context["vehicle"].ownership.owner
            context["previous_page"] = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:update_owner_step",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                    "customer_id": self.kwargs["customer_id"],
                    "vehicle_id": self.kwargs["vehicle_id"],
                    "owner_id": context["vehicle"].ownership.owner.id,
                },
            )

        return context


class QIVUpdateAmountViewSupport(
    rrgg_mixins.RrggBootstrapDisplayMixin, UpdateView
):
    model = rrgg.models.QuotationInsuranceVehicle
    fields = ["insured_amount"]
    pk_url_kwarg = "quotation_id"


class QIVUpdateStepView(QIVUpdateAmountViewSupport):
    template_name = "rrggweb/quotation/insurance/vehicle/update_step.html"

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:create_premiums",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.object.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seller"] = self.object.consultant_seller
        context["customer"] = self.object.customer
        context["vehicle"] = self.object.vehicle
        if context["vehicle"].ownership.owner is None:
            context["owner"] = "El cliente es propietario del vehículo."
            context["previous_page"] = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:define_owner",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.object.consultant_seller.id,
                    "customer_id": self.object.customer.id,
                    "vehicle_id": self.object.vehicle.id,
                },
            )
        else:
            context["owner"] = context["vehicle"].ownership.owner
            context["previous_page"] = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:update_owner_step",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.object.consultant_seller.id,
                    "customer_id": self.object.customer.id,
                    "vehicle_id": self.object.vehicle.id,
                    "owner_id": context["vehicle"].ownership.owner.id,
                },
            )
        return context


class QIVUpdateView(QIVUpdateAmountViewSupport):
    template_name = "rrggweb/quotation/insurance/vehicle/update.html"

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.object.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.object.id,
            },
        )
        return context


class QIVUpdateSellerViewSupport(
    rrgg_mixins.RrggBootstrapDisplayMixin, UpdateView
):
    model = rrgg.models.QuotationInsuranceVehicle
    fields = ["consultant_seller"]
    pk_url_kwarg = "quotation_id"


class QIVUpdateSellerView(QIVUpdateSellerViewSupport):
    template_name = "rrggweb/quotation/insurance/vehicle/update.html"

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.object.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.object.id,
            },
        )
        return context


class QIVDetailView(DetailView):
    template_name = "rrggweb/quotation/insurance/vehicle/detail.html"
    model = rrgg.models.QuotationInsuranceVehicle
    pk_url_kwarg = "quotation_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seller"] = self.object.consultant_seller
        context["customer"] = self.object.customer
        context["vehicle"] = self.object.vehicle
        if context["vehicle"].ownership.owner is None:
            context["owner"] = "El cliente es propietario del vehículo."
        else:
            context["owner"] = context["vehicle"].ownership.owner
            context["update_owner"] = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:update_owner",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "owner_id": self.object.vehicle.ownership.owner.id,
                    "quotation_id": self.object.id,
                },
            )
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:list",
            kwargs={"registrar_id": self.kwargs["registrar_id"]},
        )
        context["update_customer"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:update_customer",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "customer_id": self.object.customer.id,
                "quotation_id": self.object.id,
            },
        )
        context["update"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:update",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.object.id,
            },
        )
        context["update_vehicle"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:update_vehicle",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "vehicle_id": self.object.vehicle.id,
                "quotation_id": self.object.id,
            },
        )
        context["update_seller"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:update_seller",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.object.id,
            },
        )
        context["report_xlsx"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:report_xlsx",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.object.id,
            },
        )
        context["report_pdf"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:report_pdf",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.object.id,
            },
        )
        return context


# QUOTATION INSURANCE VEHICLE PREMIUM


class QIVPremiumsFormView(FormView):
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

        context["quotation"] = shortcuts.get_object_or_404(
            rrgg.models.QuotationInsuranceVehicle,
            id=self.kwargs["quotation_id"],
        )
        context["seller"] = context["quotation"].consultant_seller
        context["customer"] = context["quotation"].customer
        context["vehicle"] = context["quotation"].vehicle
        if context["vehicle"].ownership.owner is None:
            context["owner"] = "El cliente es propietario del vehículo."
        else:
            context["owner"] = context["vehicle"].ownership.owner
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:update_step",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.kwargs["quotation_id"],
            },
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
            "rrggweb:quotation:insurance:vehicle:detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.kwargs["quotation_id"],
            },
        )


class QIVPremiumsUpdateViewSupport(
    rrgg_mixins.RrggBootstrapDisplayMixin, UpdateView
):
    model = rrgg.models.QuotationInsuranceVehiclePremium
    fields = ["amount", "rate"]
    pk_url_kwarg = "premium_id"


class QIVPremiumsUpdateView(QIVPremiumsUpdateViewSupport):
    template_name = "rrggweb/quotation/insurance/vehicle/update_premium.html"

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.object.quotation_insurance_vehicle.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.object.quotation_insurance_vehicle.id,
            },
        )
        return context


# QUOTATION INSURANCE VEHICLE MULTIMEDIA


class QIVReportXlsxView(View):
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

        customer = quotation.customer
        ws["C6"] = f"{customer.given_name} {customer.first_surname}"

        for premium in quotation.premiums.all():
            ratio = premium.insurance_vehicle_ratio
            insurance_vehicle = ratio.insurance_vehicle
            if premium.amount > 0 and insurance_vehicle.id == 1:
                ws["E13"] = premium.amount
                ws["E14"] = ws["E13"].value * ratio.emission_right
                ws["E15"] = (ws["E13"].value + ws["E14"].value) * ratio.tax
                ws["E16"] = ws["E13"].value + ws["E14"].value + ws["E15"].value
                ws["D59"] = ratio.fee
                ws["E59"] = ws["E16"].value / ratio.fee
                ws["D60"] = ratio.direct_debit
                ws["E60"] = ws["E16"].value / ratio.direct_debit
            if premium.amount > 0 and insurance_vehicle.id == 2:
                ws["G13"] = premium.amount
                ws["G14"] = ws["G13"].value * ratio.emission_right
                ws["G15"] = (ws["G13"].value + ws["G14"].value) * ratio.tax
                ws["G16"] = ws["G13"].value + ws["G14"].value + ws["G15"].value
                ws["F59"] = ratio.fee
                ws["G59"] = ws["G16"].value / ratio.fee
                ws["F60"] = ratio.direct_debit
                ws["G60"] = ws["G16"].value / ratio.direct_debit
            if premium.amount > 0 and insurance_vehicle.id == 3:
                ws["I13"] = premium.amount
                ws["I14"] = ws["I13"].value * ratio.emission_right
                ws["I15"] = (ws["I13"].value + ws["I14"].value) * ratio.tax
                ws["I16"] = ws["I13"].value + ws["I14"].value + ws["I15"].value
                ws["H59"] = ratio.fee
                ws["I59"] = ws["I16"].value / ratio.fee
                ws["H60"] = ratio.direct_debit
                ws["I60"] = ws["I16"].value / ratio.direct_debit
            if premium.amount > 0 and insurance_vehicle.id == 4:
                ws["K13"] = premium.amount
                ws["K14"] = ws["K13"].value * ratio.emission_right
                ws["K15"] = (ws["K13"].value + ws["K14"].value) * ratio.tax
                ws["K16"] = ws["K13"].value + ws["K14"].value + ws["K15"].value
                ws["J59"] = ratio.fee
                ws["K59"] = ws["K16"].value / ratio.fee
                ws["J60"] = ratio.direct_debit
                ws["K60"] = ws["K16"].value / ratio.direct_debit
            if premium.amount > 0 and insurance_vehicle.id == 5:
                ws["M13"] = premium.amount
                ws["M14"] = ws["M13"].value * ratio.emission_right
                ws["M15"] = (ws["M13"].value + ws["M14"].value) * ratio.tax
                ws["M16"] = ws["M13"].value + ws["M14"].value + ws["M15"].value
                ws["L59"] = ratio.fee
                ws["M59"] = ws["M16"].value / ratio.fee
                ws["L60"] = ratio.direct_debit
                ws["M60"] = ws["M16"].value / ratio.direct_debit

        return wb


class QIVReportPdfView(View):
    def get(self, request, *args, **kwargs):
        from django.template.loader import render_to_string
        from weasyprint import HTML

        templatename = "rrggweb/quotation/insurance/vehicle/report.html"
        quotation = shortcuts.get_object_or_404(
            rrgg.models.QuotationInsuranceVehicle,
            id=kwargs["quotation_id"],
        )
        premiums = quotation.premiums.all().order_by(
            "insurance_vehicle_ratio__insurance_vehicle__id"
        )

        html_string = render_to_string(
            templatename,
            {
                "quotation": quotation,
                "premiums": premiums,
            },
        )

        pdf_file = HTML(string=html_string).write_pdf()

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            "attachment; filename=report_quotations.pdf"
        )

        return response


# ------------------------------

# ISSUANCE VIEW


class IssuanceView(TemplateView):
    template_name = "rrggweb/issuance.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seguros"] = [
            SeguroItem(
                "Seguro de vehicular",
                urls.reverse(
                    "rrggweb:issuance:insurance:vehicle:list",
                    kwargs={"registrar_id": self.kwargs["registrar_id"]},
                ),
            ),
            SeguroItem("Seguro de vida", ""),
            SeguroItem("Seguro de accidentes", ""),
            SeguroItem("Seguro de salud", ""),
        ]
        return context


class IssuanceInsuranceVehicleListView(ListView):
    template_name = "rrggweb/issuance/insurance/vehicle/list.html"
    model = rrgg.models.IssuanceInsuranceVehicle

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(customer__given_name__icontains=query)
            )
        return queryset


class IIVTypeFormView(FormView):
    template_name = "rrggweb/issuance/insurance/vehicle/define.html"
    form_class = forms.IssuanceTypeForm

    def form_valid(self, form):
        tipo = form.cleaned_data["tipo"]
        if tipo == "policy":
            self.success_url = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:create_policy",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "quotation_premium_id": self.kwargs[
                        "quotation_premium_id"
                    ],
                },
            )
        elif tipo == "endorsement":
            self.success_url = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:create_endorsement",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "quotation_premium_id": self.kwargs[
                        "quotation_premium_id"
                    ],
                },
            )
        else:
            messages.warning(self.request, "Debe elegir un tipo de emisión")
            return self.form_invalid(form)

        return super().form_valid(form)


class IIVCreatePolicyView(rrgg_mixins.RrggBootstrapDisplayMixin, CreateView):
    template_name = "rrggweb/issuance/insurance/vehicle/create.html"
    model = rrgg.models.IssuanceInsuranceVehiclePolicy
    fields = [
        "number_registry",
        "issuance_date",
        "initial_validity",
        "final_validity",
    ]

    def form_valid(self, form):
        form.instance.quotation_vehicle_premium_id = self.kwargs[
            "quotation_premium_id"
        ]
        # validate expiration date
        quotation_premium = shortcuts.get_object_or_404(
            rrgg.models.QuotationInsuranceVehiclePremium,
            id=self.kwargs["quotation_premium_id"],
        )
        if quotation_premium.quotation_insurance_vehicle.expired:
            messages.warning(self.request, "Esta cotización ya expiró")
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quotation_premium"] = shortcuts.get_object_or_404(
            rrgg.models.QuotationInsuranceVehiclePremium,
            id=self.kwargs["quotation_premium_id"],
        )
        return context

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:create_document",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "issuance_id": self.object.id,
            },
        )


class IIVCreateEndorsementView(
    rrgg_mixins.RrggBootstrapDisplayMixin, CreateView
):
    template_name = "rrggweb/issuance/insurance/vehicle/create.html"
    model = rrgg.models.IssuanceInsuranceVehicleEndorsement
    fields = [
        "number_registry",
        "issuance_date",
        "initial_validity",
        "commission",
    ]

    def form_valid(self, form):
        form.instance.quotation_vehicle_premium_id = self.kwargs[
            "quotation_premium_id"
        ]
        # validate expiration date
        quotation_premium = shortcuts.get_object_or_404(
            rrgg.models.QuotationInsuranceVehiclePremium,
            id=self.kwargs["quotation_premium_id"],
        )
        if quotation_premium.quotation_insurance_vehicle.expired:
            messages.warning(self.request, "Esta cotización ya expiró")
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quotation_premium"] = shortcuts.get_object_or_404(
            rrgg.models.QuotationInsuranceVehiclePremium,
            id=self.kwargs["quotation_premium_id"],
        )
        return context

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:create_document",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "issuance_id": self.object.id,
            },
        )


class IssuanceInsuranceVehicleDetailIssuanceView(DetailView):
    template_name = "rrggweb/issuance/insurance/vehicle/detail.html"
    model = rrgg.models.IssuanceInsuranceVehicle
    pk_url_kwarg = "issuance_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["documents"] = self.object.documents.all()
        return context


class IssuanceInsuranceVehicleUpdateIssuanceView(
    rrgg_mixins.RrggBootstrapDisplayMixin, UpdateView
):
    template_name = "rrggweb/issuance/insurance/vehicle/update.html"
    model = rrgg.models.IssuanceInsuranceVehicle
    fields = [
        "issuance_date",
        "initial_validity",
        "final_validity",
    ]
    pk_url_kwarg = "issuance_id"

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:list",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
            },
        )


class IIVStatusFormView(FormView):
    template_name = "rrggweb/issuance/insurance/vehicle/define.html"
    form_class = forms.IssuanceTypeForm

    def form_valid(self, form):
        tipo = form.cleaned_data["tipo"]
        if tipo == "policy":
            self.success_url = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:create_policy",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "quotation_premium_id": self.kwargs[
                        "quotation_premium_id"
                    ],
                },
            )
        elif tipo == "endorsement":
            self.success_url = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:create_endorsement",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "quotation_premium_id": self.kwargs[
                        "quotation_premium_id"
                    ],
                },
            )
        else:
            messages.warning(self.request, "Debe elegir un tipo de emisión")
            return self.form_invalid(form)

        return super().form_valid(form)


class IIVUpdateStatusFormView(FormView):
    template_name = "rrggweb/issuance/insurance/vehicle/status.html"
    form_class = forms.IssuanceStatusForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["comment"].required = False
        return form

    def form_valid(self, form: forms.IssuanceStatusForm):
        issuance = shortcuts.get_object_or_404(
            rrgg.models.IssuanceInsuranceVehicle,
            id=self.kwargs["issuance_id"],
        )
        data = form.cleaned_data
        issuance.status = data["status"]
        issuance.comment = data["comment"]
        issuance.save()
        return super().form_valid(form)

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "issuance_id": self.kwargs["issuance_id"],
            },
        )


class IssuanceInsuranceVehicleAddDocumentCreateView(
    rrgg_mixins.RrggBootstrapDisplayMixin, CreateView
):
    template_name = "rrggweb/issuance/insurance/vehicle/create_document.html"
    model = rrgg.models.IssuanceInsuranceVehicleDocument
    fields = ["issuance", "file"]

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:create_document",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "issuance_id": self.kwargs["issuance_id"],
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["documents"] = self.model.objects.filter(
            issuance_id=self.kwargs["issuance_id"]
        )
        return context


class IssuanceInsuranceVehicleDeleteDocumentView(DeleteView):
    template_name = "rrggweb/issuance/insurance/vehicle/delete_document.html"
    model = rrgg.models.IssuanceInsuranceVehicleDocument
    pk_url_kwarg = "document_id"

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:create_document",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "issuance_id": self.kwargs["issuance_id"],
            },
        )


# ------------------------------

# COLLECTION VIEW


class CollectionView(TemplateView):
    template_name = "rrggweb/collection.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seguros"] = [
            SeguroItem(
                "Seguro de vehicular",
                urls.reverse(
                    "rrggweb:collection:insurance:vehicle:list",
                    kwargs={"registrar_id": self.kwargs["registrar_id"]},
                ),
            ),
            SeguroItem("Seguro de vida", ""),
            SeguroItem("Seguro de accidentes", ""),
            SeguroItem("Seguro de salud", ""),
        ]
        return context


class CollectionInsuranceVehicleListView(ListView):
    template_name = "rrggweb/collection/insurance/vehicle/list.html"
    model = rrgg.models.CollectionInsuranceVehicle


class CollectionInsuranceVehicleCreateCollectionView(
    rrgg_mixins.RrggBootstrapDisplayMixin, CreateView
):
    template_name = (
        "rrggweb/collection/insurance/vehicle/create_collection.html"
    )
    model = rrgg.models.CollectionInsuranceVehicle
    fields = [
        "expiration_date",
        "payment_date",
        "payment_receipt",
        "issue",
        "amount",
    ]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["payment_date"].required = False
        form.fields["payment_receipt"].required = False
        return form

    def form_valid(self, form):
        form.instance.issuance_vehicle_id = self.kwargs["issuance_id"]
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["issuance"] = shortcuts.get_object_or_404(
            rrgg.models.IssuanceInsuranceVehicle,
            id=self.kwargs["issuance_id"],
        )
        return context

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:collection:insurance:vehicle:list",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
            },
        )
