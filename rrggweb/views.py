import re

from django import shortcuts, urls
from django.contrib import messages
from django.contrib.auth import views as views_auth
from django.contrib.auth.mixins import LoginRequiredMixin
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
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "COTIZACIÓN VEHICULAR"
        context["subtitle"] = "Lista de cotizaciones"
        context["new_register"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:select_role",
            kwargs={"registrar_id": self.kwargs["registrar_id"]},
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation",
            kwargs={"registrar_id": self.kwargs["registrar_id"]},
        )
        return context


# SELLER


class QIVSelectRoleFormView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/seller_form.html"
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
        context["title"] = "COTIZACIÓN VEHICULAR"
        context["subtitle"] = "Seleccionar responsable"
        context["initial_step"] = 1
        context["final_step"] = 6
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:list",
            kwargs={"registrar_id": self.kwargs["registrar_id"]},
        )
        return context


class QIVSelectSellerFormView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/seller_form.html"
    form_class = forms.SellerForm

    def form_valid(self, form: forms.SellerForm):
        seller = form.cleaned_data["asesores"]
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
        context["title"] = "COTIZACIÓN VEHICULAR"
        context["subtitle"] = "Seleccionar responsable"
        context["initial_step"] = 1
        context["final_step"] = 6
        context["role_selector"] = forms.RoleForm(
            role_id=self.kwargs.get("role_id")
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:select_role",
            kwargs={"registrar_id": self.kwargs["registrar_id"]},
        )
        return context


class QIVUpdateSellerViewSupport(
    rrgg_mixins.RrggBootstrapDisplayMixin, UpdateView
):
    template_name = "rrggweb/quotation/insurance/vehicle/seller_form.html"
    model = rrgg.models.QuotationInsuranceVehicle
    fields = ["consultant_seller"]
    pk_url_kwarg = "quotation_id"


class QIVUpdateSellerView(QIVUpdateSellerViewSupport):
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
        context["title"] = "COTIZACIÓN VEHICULAR"
        context["subtitle"] = "Cambiar asesor"
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.object.id,
            },
        )
        return context


# QUOTATION - CLIENT


class QIVSearchCustomerView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/customer_form.html"
    form_class = forms.SearchPersonForm

    def form_valid(self, form):
        document_number = form.cleaned_data["document_number"]
        if not re.match("^[0-9]+$", document_number):
            form.add_error(
                "document_number",
                "El número de documento debe contener solo números.",
            )
            return super().form_invalid(form)
        natural_customer_exists = (
            rrgg.models.CustomerMembership.objects.filter(
                natural_person__document_number=document_number
            ).exists()
        )
        legal_customer_exists = rrgg.models.CustomerMembership.objects.filter(
            legal_person__document_number=document_number
        ).exists()
        if natural_customer_exists:
            customer = rrgg.models.CustomerMembership.objects.get(
                natural_person__document_number=document_number
            )
            self.success_url = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:search_vehicle",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                    "customer_id": customer.id,
                },
            )
        elif legal_customer_exists:
            customer = rrgg.models.CustomerMembership.objects.get(
                legal_person__document_number=document_number
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
            select_customer_url = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:select_customer",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                },
            )
            self.success_url = (
                f"{select_customer_url}?document_number={document_number}"
            )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "COTIZACIÓN VEHICULAR"
        context["subtitle"] = "Buscar contratante"
        context["initial_step"] = 2
        context["final_step"] = 6
        context["body"] = "Buscar contratante"
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:select_role",
            kwargs={"registrar_id": self.kwargs["registrar_id"]},
        )
        return context


class QIVSelectCustomerFormView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/customer_form.html"
    form_class = forms.SelectCustomerForm

    def form_valid(self, form: forms.SelectCustomerForm):
        type_customer = form.cleaned_data["type_customer"]
        dn = self.request.GET.get("document_number", "")
        if type_customer == "persona_natural":
            create_customer_url = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:create_natural_person",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                },
            )
            self.success_url = f"{create_customer_url}?document_number={dn}"
        elif type_customer == "persona_jurídica":
            create_customer_url = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:create_legal_person",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                },
            )
            self.success_url = f"{create_customer_url}?document_number={dn}"
        else:
            pass
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "COTIZACIÓN VEHICULAR"
        context["subtitle"] = "Definir contratante"
        context["initial_step"] = 2
        context["final_step"] = 6
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


class QIVCreateCustomerView(
    LoginRequiredMixin, rrgg_mixins.RrggBootstrapDisplayMixin, CreateView
):
    template_name = "rrggweb/quotation/insurance/vehicle/customer_form.html"
    fields = "__all__"

    def get_initial(self):
        initial = super().get_initial()
        initial["document_number"] = self.request.GET.get(
            "document_number", ""
        )
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "COTIZACIÓN VEHICULAR"
        context["subtitle"] = "Registrar contratante"
        context["body"] = "Formulario del Contratante:"
        context["initial_step"] = 2
        context["final_step"] = 6
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:select_customer",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
            },
        )
        return context


class QIVCreateNaturalPersonView(QIVCreateCustomerView):
    model = rrgg.models.NaturalPerson

    def get_initial(self):
        initial = super().get_initial()
        dni = rrgg.models.DocumentType.objects.get(code="dni")
        initial["document_type"] = dni
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["second_surname"].required = False
        return form

    def get_success_url(self):
        rrgg.models.CustomerMembership.objects.create(
            natural_person=self.object
        )
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:search_vehicle",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.object.membership.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type_customer"] = "Persona natural"
        return context


class QIVCreateLegalPersonView(QIVCreateCustomerView):
    model = rrgg.models.LegalPerson

    def get_initial(self):
        initial = super().get_initial()
        ruc = rrgg.models.DocumentType.objects.get(code="ruc")
        initial["document_type"] = ruc
        return initial

    def get_success_url(self):
        rrgg.models.CustomerMembership.objects.create(legal_person=self.object)
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:search_vehicle",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.object.membership.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type_customer"] = "Persona jurídica"
        return context


class QIVUpdateNaturalPersonViewSupport(
    rrgg_mixins.RrggBootstrapDisplayMixin, UpdateView
):
    template_name = "rrggweb/quotation/insurance/vehicle/customer_form.html"
    pk_url_kwarg = "natural_person_id"
    model = rrgg.models.NaturalPerson
    fields = "__all__"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["second_surname"].required = False
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "COTIZACIÓN VEHICULAR"
        context["subtitle"] = "Editar contratante"
        return context


class QIVUpdateNaturalPersonStepView(QIVUpdateNaturalPersonViewSupport):
    def get_success_url(self):
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:search_vehicle",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.object.membership.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["initial_step"] = 2
        context["final_step"] = 6
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


class QIVUpdateNaturalPersonView(QIVUpdateNaturalPersonViewSupport):
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


class QIVUpdateLegalPersonViewSupport(
    rrgg_mixins.RrggBootstrapDisplayMixin, UpdateView
):
    template_name = "rrggweb/quotation/insurance/vehicle/customer_form.html"
    pk_url_kwarg = "legal_person_id"
    model = rrgg.models.LegalPerson
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "COTIZACIÓN VEHICULAR"
        context["subtitle"] = "Editar contratante"
        return context


class QIVUpdateLegalPersonStepView(QIVUpdateLegalPersonViewSupport):
    def get_success_url(self):
        return urls.reverse(
            "rrggweb:quotation:insurance:vehicle:search_vehicle",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.object.membership.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["initial_step"] = 2
        context["final_step"] = 6
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


class QIVUpdateLegalPersonView(QIVUpdateLegalPersonViewSupport):
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


# QUOTATION - VEHICLE


class QIVSearchVehicleView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/vehicle_form.html"
    form_class = forms.SearchVehicleForm

    def form_valid(self, form):
        plate = form.cleaned_data["plate"]
        vehicle_exists = rrgg.models.Vehicle.objects.filter(
            plate=plate
        ).exists()
        if vehicle_exists:
            vehicle = rrgg.models.Vehicle.objects.get(plate=plate)
            vehicle_ownership_exists = (
                rrgg.models.VehicleOwnership.objects.filter(
                    vehicle__plate=plate
                ).exists()
            )
            if vehicle_ownership_exists:
                if isinstance(
                    vehicle.ownership.pick, rrgg.models.CustomerMembership
                ):
                    customer = shortcuts.get_object_or_404(
                        rrgg.models.CustomerMembership,
                        id=self.kwargs["customer_id"],
                    )
                    if vehicle.ownership.pick == customer.pick:
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
                        form.add_error(
                            "plate",
                            "El contratante no es dueño del vehículo",
                        )
                        return super().form_invalid(form)
                else:
                    # toca evaluar si el propietario registrado es el actual
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
        context["title"] = "COTIZACIÓN VEHICULAR"
        context["subtitle"] = "Buscar vehículo"
        context["initial_step"] = 3
        context["final_step"] = 6
        context["pretty_style"] = False
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.CustomerMembership, id=self.kwargs["customer_id"]
        )
        # determinar si el contratante es persona natural o jurídica
        customer = shortcuts.get_object_or_404(
            rrgg.models.CustomerMembership, id=self.kwargs["customer_id"]
        )
        person = customer.pick
        if isinstance(person, rrgg.models.NaturalPerson):
            context["previous_page"] = urls.reverse(
                (
                    "rrggweb:quotation:insurance:vehicle:"
                    "update_natural_person_step"
                ),
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                    "natural_person_id": person.id,
                },
            )
        elif isinstance(person, rrgg.models.LegalPerson):
            context["previous_page"] = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:update_legal_person_step",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                    "legal_person_id": person.id,
                },
            )
        else:
            pass

        return context


class QIVCreateVehicleView(rrgg_mixins.RrggBootstrapDisplayMixin, CreateView):
    template_name = "rrggweb/quotation/insurance/vehicle/vehicle_form.html"
    model = rrgg.models.Vehicle
    fields = "__all__"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["plate"].required = False
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
        context["title"] = "COTIZACIÓN VEHICULAR"
        context["subtitle"] = "Registrar vehículo"
        context["initial_step"] = 3
        context["final_step"] = 6
        context["pretty_style"] = True
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.CustomerMembership, id=self.kwargs["customer_id"]
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
    template_name = "rrggweb/quotation/insurance/vehicle/vehicle_form.html"
    model = rrgg.models.Vehicle
    fields = "__all__"
    pk_url_kwarg = "vehicle_id"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["has_gps"].required = False
        form.fields["has_endorsee"].required = False
        form.fields["endorsee_bank"].required = False
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "COTIZACIÓN VEHICULAR"
        context["subtitle"] = "Editar vehículo"
        return context


class QIVUpdateVehicleStepView(QIVUpdateVehicleViewSupport):
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
        context["initial_step"] = 3
        context["final_step"] = 6
        context["pretty_style"] = True
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.CustomerMembership, id=self.kwargs["customer_id"]
        )
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
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


class QIVUpdateVehicleView(QIVUpdateVehicleViewSupport):
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
        context["pretty_style"] = True
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.kwargs["quotation_id"],
            },
        )
        return context


# QUOTATION - OWNER


class QIVDefineOwnerView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/owner_form.html"
    form_class = forms.DefineOwnerForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["is_owner"].required = False
        return form

    def form_valid(self, form):
        vehicle = shortcuts.get_object_or_404(
            rrgg.models.Vehicle, id=self.kwargs["vehicle_id"]
        )
        vehicle_ownership_exists = rrgg.models.VehicleOwnership.objects.filter(
            vehicle=vehicle
        ).exists()
        if vehicle_ownership_exists:
            vehicle.ownership.delete()
        else:
            pass

        is_customer_owner = form.cleaned_data["is_owner"]
        if is_customer_owner:
            customer = shortcuts.get_object_or_404(
                rrgg.models.CustomerMembership, id=self.kwargs["customer_id"]
            )
            rrgg.models.VehicleOwnership.objects.create(
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
        context["title"] = "COTIZACIÓN VEHICULAR"
        context["subtitle"] = "Definir propietario"
        context["initial_step"] = 4
        context["final_step"] = 6
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.CustomerMembership, id=self.kwargs["customer_id"]
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
    template_name = "rrggweb/quotation/insurance/vehicle/owner_form.html"
    form_class = forms.SearchPersonForm

    def form_valid(self, form):
        document_number = form.cleaned_data["document_number"]
        if not re.match("^[0-9]+$", document_number):
            form.add_error(
                "document_number",
                "El número de documento debe contener solo números.",
            )
            return super().form_invalid(form)
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
            rrgg.models.VehicleOwnership.objects.create(
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
        context["title"] = "COTIZACIÓN VEHICULAR"
        context["subtitle"] = "Buscar propietario"
        context["initial_step"] = 4
        context["final_step"] = 6
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.CustomerMembership, id=self.kwargs["customer_id"]
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
    template_name = "rrggweb/quotation/insurance/vehicle/owner_form.html"
    model = rrgg.models.Owner
    fields = "__all__"

    def get_success_url(self):
        vehicle = shortcuts.get_object_or_404(
            rrgg.models.Vehicle, id=self.kwargs["vehicle_id"]
        )
        rrgg.models.VehicleOwnership.objects.create(
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
        context["title"] = "COTIZACIÓN VEHICULAR"
        context["subtitle"] = "Registrar propietario"
        context["body"] = "Formulario del Propietario:"
        context["initial_step"] = 4
        context["final_step"] = 6
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.CustomerMembership, id=self.kwargs["customer_id"]
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
    template_name = "rrggweb/quotation/insurance/vehicle/owner_form.html"
    model = rrgg.models.Owner
    fields = "__all__"
    pk_url_kwarg = "owner_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "COTIZACIÓN VEHICULAR"
        context["subtitle"] = "Editar propietario"
        return context


class QIVUpdateOwnerStepView(QIVUpdateOwnerViewSupport):
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
        context["initial_step"] = 4
        context["final_step"] = 6
        context["body"] = "Formulario del Propietario:"
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.CustomerMembership, id=self.kwargs["customer_id"]
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
    template_name = "rrggweb/quotation/insurance/vehicle/form.html"
    model = rrgg.models.QuotationInsuranceVehicle
    fields = ["insured_amount", "currency"]

    def form_valid(self, form):
        form.instance.risk = rrgg.models.Risk.objects.get(name="Vehicular")
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
        context["title"] = "COTIZACIÓN VEHICULAR"
        context["subtitle"] = "Registrar cotización"
        context["initial_step"] = 5
        context["final_step"] = 6
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.CustomerMembership, id=self.kwargs["customer_id"]
        )
        context["vehicle"] = shortcuts.get_object_or_404(
            rrgg.models.Vehicle, id=self.kwargs["vehicle_id"]
        )
        context["owner"] = context["vehicle"].ownership

        if isinstance(context["owner"].pick, rrgg.models.Owner):
            context["previous_page"] = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:update_owner_step",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                    "customer_id": self.kwargs["customer_id"],
                    "vehicle_id": self.kwargs["vehicle_id"],
                    "owner_id": context["owner"].owner.id,
                },
            )
        else:
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


class QIVUpdateAmountViewSupport(
    rrgg_mixins.RrggBootstrapDisplayMixin, UpdateView
):
    template_name = "rrggweb/quotation/insurance/vehicle/form.html"
    model = rrgg.models.QuotationInsuranceVehicle
    fields = ["insured_amount", "currency"]
    pk_url_kwarg = "quotation_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "COTIZACIÓN VEHICULAR"
        context["subtitle"] = "Editar cotización"
        return context


class QIVUpdateStepView(QIVUpdateAmountViewSupport):
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
        context["initial_step"] = 5
        context["final_step"] = 6
        context["seller"] = self.object.consultant_seller
        context["customer"] = self.object.customer
        context["vehicle"] = self.object.vehicle
        context["owner"] = context["vehicle"].ownership

        if isinstance(context["owner"].pick, rrgg.models.Owner):
            context["previous_page"] = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:update_owner_step",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.object.consultant_seller.id,
                    "customer_id": self.object.customer.id,
                    "vehicle_id": self.object.vehicle.id,
                    "owner_id": context["owner"].owner.id,
                },
            )
        else:
            context["previous_page"] = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:define_owner",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.object.consultant_seller.id,
                    "customer_id": self.object.customer.id,
                    "vehicle_id": self.object.vehicle.id,
                },
            )
        return context


class QIVUpdateView(QIVUpdateAmountViewSupport):
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
        context["title"] = "COTIZACIÓN VEHICULAR"
        context["subtitle"] = "Detalle de la cotización"
        context["seller"] = self.object.consultant_seller
        context["customer"] = self.object.customer
        context["vehicle"] = self.object.vehicle
        context["owner"] = context["vehicle"].ownership
        if isinstance(context["owner"].pick, rrgg.models.Owner):
            context["update_owner"] = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:update_owner",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "owner_id": context["owner"].owner.id,
                    "quotation_id": self.object.id,
                },
            )
        else:
            pass
        context["title"] = "COTIZACIÓN VEHICULAR"
        context["subtitle"] = "Detalle de la cotización"
        context["previous_page"] = urls.reverse(
            "rrggweb:quotation:insurance:vehicle:list",
            kwargs={"registrar_id": self.kwargs["registrar_id"]},
        )
        # determinar si el contratante es persona natural o jurídica
        customer = shortcuts.get_object_or_404(
            rrgg.models.CustomerMembership, id=self.object.customer.id
        )
        person = customer.pick
        if isinstance(person, rrgg.models.NaturalPerson):
            context["update_customer"] = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:update_natural_person",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "natural_person_id": person.id,
                    "quotation_id": self.object.id,
                },
            )
        elif isinstance(person, rrgg.models.LegalPerson):
            context["update_customer"] = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:update_legal_person",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "legal_person_id": person.id,
                    "quotation_id": self.object.id,
                },
            )
        else:
            pass

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
        context["step"] = True
        context["title"] = "COTIZACIÓN VEHICULAR"
        context["subtitle"] = "Registrar primas de aseguradoras"
        context["quotation"] = shortcuts.get_object_or_404(
            rrgg.models.QuotationInsuranceVehicle,
            id=self.kwargs["quotation_id"],
        )
        context["insurances"] = rrgg.models.InsuranceVehicle.objects.all()
        context["seller"] = context["quotation"].consultant_seller
        context["customer"] = context["quotation"].customer
        context["vehicle"] = context["quotation"].vehicle
        context["owner"] = context["vehicle"].ownership
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
    template_name = "rrggweb/quotation/insurance/vehicle/update_premium.html"
    model = rrgg.models.QuotationInsuranceVehiclePremium
    fields = ["amount", "rate"]
    pk_url_kwarg = "premium_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["insured_amount"] = (
            self.object.quotation_insurance_vehicle.insured_amount
        )
        return context


class QIVPremiumsUpdateView(QIVPremiumsUpdateViewSupport):
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
        context["title"] = "COTIZACIÓN VEHICULAR"
        context["subtitle"] = "Editar Prima de Aseguradora"
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
        ws["C6"] = str(quotation.customer)

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
        my_range = range(1, 6)

        html_string = render_to_string(
            templatename,
            {
                "quotation": quotation,
                "premiums": premiums,
                "my_range": my_range,
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


# LIST


class IIVListView(ListView):
    template_name = "rrggweb/issuance/insurance/vehicle/list.html"
    model = rrgg.models.IssuanceInsuranceVehicle
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Lista de emisiones"
        context["new_register"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:define_record_type",
            kwargs={"registrar_id": self.kwargs["registrar_id"]},
        )
        return context


class IIVDetailIssuanceView(DetailView):
    template_name = "rrggweb/issuance/insurance/vehicle/detail.html"
    model = rrgg.models.IssuanceInsuranceVehicle
    pk_url_kwarg = "issuance_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Detalle de la emisión"
        context["quotation_premium"] = self.object.quotation_vehicle_premium
        context["ratio"] = context["quotation_premium"].insurance_vehicle_ratio
        context["quotation"] = context[
            "quotation_premium"
        ].quotation_insurance_vehicle
        context["customer"] = context["quotation"].customer
        context["vehicle"] = context["quotation"].vehicle
        context["owner"] = context["vehicle"].ownership
        if isinstance(context["owner"].pick, rrgg.models.Owner):
            context["update_owner"] = urls.reverse(
                "rrggweb:quotation:insurance:vehicle:update_owner",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "owner_id": context["owner"].owner.id,
                    "quotation_id": self.object.id,
                },
            )
        context["seller"] = self.object.consultant_seller
        context["seller_commission"] = round(
            context["seller"].commission_rate.new_sale
            * self.object.net_commission_amount,
            2,
        )
        context["kcs_commission"] = round(
            self.object.net_commission_amount - context["seller_commission"], 2
        )
        context["documents"] = self.object.documents.all()
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:list",
            kwargs={"registrar_id": self.kwargs["registrar_id"]},
        )
        context["anular"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:update_status",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "issuance_id": self.kwargs["issuance_id"],
            },
        )
        return context


# TYPE ISSUANCE


class IIVDefineRegistrationTypeView(FormView):
    template_name = "rrggweb/issuance/insurance/vehicle/basic_form.html"
    form_class = forms.SelectVehicleRegistrationTypeForm

    def form_valid(self, form):
        vehicle_registration_type = form.cleaned_data[
            "vehicle_registration_type"
        ]
        if vehicle_registration_type == "new_sale":
            self.success_url = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:define_new_sale",
                kwargs={"registrar_id": self.kwargs["registrar_id"]},
            )
        elif vehicle_registration_type == "renewal":
            self.success_url = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:define_record_type",
                kwargs={"registrar_id": self.kwargs["registrar_id"]},
            )
        else:
            pass
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Definir tipo de registro"
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:list",
            kwargs={"registrar_id": self.kwargs["registrar_id"]},
        )
        return context


class IIVDefineNewSaleView(FormView):
    template_name = "rrggweb/issuance/insurance/vehicle/basic_form.html"
    form_class = forms.DefineNewSaleForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["has_quote"].required = False
        return form

    def form_valid(self, form):
        has_quote = form.cleaned_data["has_quote"]
        if has_quote:
            self.success_url = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:list_quotations",
                kwargs={"registrar_id": self.kwargs["registrar_id"]},
            )
        else:
            self.success_url = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:select_role_ns",
                kwargs={"registrar_id": self.kwargs["registrar_id"]},
            )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Definir venta nueva"
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:define_record_type",
            kwargs={"registrar_id": self.kwargs["registrar_id"]},
        )
        return context


class IIVListQuotationView(ListView):
    template_name = "rrggweb/issuance/insurance/vehicle/list_quotations.html"
    model = rrgg.models.QuotationInsuranceVehicle
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Lista de cotizaciones vehiculares"
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:define_new_sale",
            kwargs={"registrar_id": self.kwargs["registrar_id"]},
        )
        return context


class IIVQuotationDetailView(DetailView):
    template_name = "rrggweb/quotation/insurance/vehicle/detail.html"
    model = rrgg.models.QuotationInsuranceVehicle
    pk_url_kwarg = "quotation_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Detalle del registro vehicular"
        context["customer"] = self.object.customer
        context["vehicle"] = self.object.vehicle
        context["owner"] = context["vehicle"].ownership
        if isinstance(context["owner"].pick, rrgg.models.Owner):
            context["update_owner"] = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:update_owner",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "owner_id": context["owner"].owner.id,
                    "quotation_id": self.object.id,
                },
            )
        else:
            pass
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:list_quotations",
            kwargs={"registrar_id": self.kwargs["registrar_id"]},
        )
        # determinar si el contratante es persona natural o jurídica
        customer = shortcuts.get_object_or_404(
            rrgg.models.CustomerMembership, id=self.object.customer.id
        )
        person = customer.pick
        if isinstance(person, rrgg.models.NaturalPerson):
            context["update_customer"] = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:update_natural_person",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "natural_person_id": person.id,
                    "quotation_id": self.object.id,
                },
            )
        elif isinstance(person, rrgg.models.LegalPerson):
            context["update_customer"] = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:update_legal_person",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "legal_person_id": person.id,
                    "quotation_id": self.object.id,
                },
            )
        else:
            pass

        context["update"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:update_quotation",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.object.id,
            },
        )
        context["update_vehicle"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:update_vehicle",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "vehicle_id": self.object.vehicle.id,
                "quotation_id": self.object.id,
            },
        )
        return context


# ISSUANCE - QUOTATION


class IIVSelectRoleQFormView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/seller_form.html"
    form_class = forms.RoleForm

    def form_valid(self, form: forms.RoleForm):
        role = form.cleaned_data["roles"]
        self.success_url = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:select_seller_q",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "premium_id": self.kwargs["premium_id"],
                "role_id": role.id,
            },
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Seleccionar responsable de la emisión"
        context["initial_step"] = 1
        context["final_step"] = 4
        premium = shortcuts.get_object_or_404(
            rrgg.models.QuotationInsuranceVehiclePremium,
            id=self.kwargs["premium_id"],
        )
        quotation = premium.quotation_insurance_vehicle
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:quotation_detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": quotation.id,
            },
        )
        return context


class IIVSelectSellerQFormView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/seller_form.html"
    form_class = forms.SellerForm

    def form_valid(self, form: forms.SellerForm):
        seller = form.cleaned_data["asesores"]
        self.success_url = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:select_plan_q",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "premium_id": self.kwargs["premium_id"],
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
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Seleccionar responsable de la emisión"
        context["initial_step"] = 1
        context["final_step"] = 4
        context["role_selector"] = forms.RoleForm(
            role_id=self.kwargs.get("role_id")
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:select_role_q",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "premium_id": self.kwargs["premium_id"],
            },
        )
        return context


class IIVPlanFormViewSupport(FormView):
    template_name = "rrggweb/issuance/insurance/vehicle/basic_form.html"
    form_class = forms.InsurancePlanForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        qivp = shortcuts.get_object_or_404(
            rrgg.models.QuotationInsuranceVehiclePremium,
            id=self.kwargs["premium_id"],
        )
        ivr = qivp.insurance_vehicle_ratio
        riv = shortcuts.get_object_or_404(
            rrgg.models.RiskInsuranceVehicle,
            insurance_vehicle_id=ivr.insurance_vehicle_id,
            risk_id=qivp.quotation_insurance_vehicle.risk_id,
        )
        kwargs["riv_id"] = riv.id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Seleccionar plan de seguro"
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        riv = shortcuts.get_object_or_404(
            rrgg.models.RiskInsuranceVehicle,
            id=self.get_form_kwargs()["riv_id"],
        )
        context["risk_selector"] = forms.RiskForm(risk_id=riv.risk_id)
        context["insurance_vehicle_selector"] = forms.InsuranceVehicleForm(
            iv_id=riv.insurance_vehicle_id
        )
        return context


class IIVPlanFormQView(IIVPlanFormViewSupport):
    def form_valid(self, form: forms.InsurancePlanForm):
        plan = form.cleaned_data["planes de seguro"]
        self.success_url = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:create_step_q",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "premium_id": self.kwargs["premium_id"],
                "seller_id": self.kwargs["seller_id"],
                "plan_id": plan.id,
            },
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["initial_step"] = 2
        context["final_step"] = 4
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:select_role_q",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "premium_id": self.kwargs["premium_id"],
            },
        )
        return context


class IIVPlanFormNSView(IIVPlanFormViewSupport):
    def form_valid(self, form: forms.InsurancePlanForm):
        plan = form.cleaned_data["planes de seguro"]
        self.success_url = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:create_step_ns",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "premium_id": self.kwargs["premium_id"],
                "seller_id": self.kwargs["seller_id"],
                "plan_id": plan.id,
            },
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["initial_step"] = 7
        context["final_step"] = 9
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:update_premium_step",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "premium_id": self.kwargs["premium_id"],
                "seller_id": self.kwargs["seller_id"],
            },
        )
        return context


# ISSUANCE - NEW SALE


class IIVSelectRoleNSFormView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/seller_form.html"
    form_class = forms.RoleForm

    def form_valid(self, form: forms.RoleForm):
        role = form.cleaned_data["roles"]
        self.success_url = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:select_seller_ns",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "role_id": role.id,
            },
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Seleccionar responsable de la emisión"
        context["initial_step"] = 1
        context["final_step"] = 9
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:define_new_sale",
            kwargs={"registrar_id": self.kwargs["registrar_id"]},
        )
        return context


class IIVSelectSellerNSFormView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/seller_form.html"
    form_class = forms.SellerForm

    def form_valid(self, form: forms.SellerForm):
        seller = form.cleaned_data["asesores"]
        self.success_url = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:search_customer",
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
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Seleccionar responsable de la emisión"
        context["initial_step"] = 1
        context["final_step"] = 9
        context["role_selector"] = forms.RoleForm(
            role_id=self.kwargs.get("role_id")
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:select_role_ns",
            kwargs={"registrar_id": self.kwargs["registrar_id"]},
        )
        return context


# NEW SALE - CLIENT


class IIVSearchCustomerView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/customer_form.html"
    form_class = forms.SearchPersonForm

    def form_valid(self, form):
        document_number = form.cleaned_data["document_number"]
        if not re.match("^[0-9]+$", document_number):
            form.add_error(
                "document_number",
                "El número de documento debe contener solo números.",
            )
            return super().form_invalid(form)
        natural_customer_exists = (
            rrgg.models.CustomerMembership.objects.filter(
                natural_person__document_number=document_number
            ).exists()
        )
        legal_customer_exists = rrgg.models.CustomerMembership.objects.filter(
            legal_person__document_number=document_number
        ).exists()
        if natural_customer_exists:
            customer = rrgg.models.CustomerMembership.objects.get(
                natural_person__document_number=document_number
            )
            self.success_url = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:search_vehicle",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                    "customer_id": customer.id,
                },
            )
        elif legal_customer_exists:
            customer = rrgg.models.CustomerMembership.objects.get(
                legal_person__document_number=document_number
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
            select_customer_url = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:select_customer",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                },
            )
            self.success_url = (
                f"{select_customer_url}?document_number={document_number}"
            )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Buscar contratante"
        context["initial_step"] = 2
        context["final_step"] = 9
        context["body"] = "Buscar contratante"
        seller = shortcuts.get_object_or_404(
            rrgg.models.Consultant,
            id=self.kwargs["seller_id"],
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:select_seller_ns",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "role_id": seller.role.id,
            },
        )
        return context


class IIVSelectCustomerFormView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/customer_form.html"
    form_class = forms.SelectCustomerForm

    def form_valid(self, form: forms.SelectCustomerForm):
        type_customer = form.cleaned_data["type_customer"]
        dn = self.request.GET.get("document_number", "")
        if type_customer == "persona_natural":
            create_customer_url = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:create_natural_person",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                },
            )
            self.success_url = f"{create_customer_url}?document_number={dn}"
        elif type_customer == "persona_jurídica":
            create_customer_url = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:create_legal_person",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                },
            )
            self.success_url = f"{create_customer_url}?document_number={dn}"
        else:
            pass
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Definir contratante"
        context["initial_step"] = 2
        context["final_step"] = 9
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:search_customer",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
            },
        )
        return context


class IIVCreateCustomerView(
    LoginRequiredMixin, rrgg_mixins.RrggBootstrapDisplayMixin, CreateView
):
    template_name = "rrggweb/quotation/insurance/vehicle/customer_form.html"
    fields = "__all__"

    def get_initial(self):
        initial = super().get_initial()
        initial["document_number"] = self.request.GET.get(
            "document_number", ""
        )
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Registrar contratante"
        context["body"] = "Formulario del Contratante:"
        context["initial_step"] = 2
        context["final_step"] = 9
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:select_customer",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
            },
        )
        return context


class IIVCreateNaturalPersonView(IIVCreateCustomerView):
    model = rrgg.models.NaturalPerson

    def get_initial(self):
        initial = super().get_initial()
        dni = rrgg.models.DocumentType.objects.get(code="dni")
        initial["document_type"] = dni
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["second_surname"].required = False
        return form

    def get_success_url(self):
        rrgg.models.CustomerMembership.objects.create(
            natural_person=self.object
        )
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:search_vehicle",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.object.membership.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type_customer"] = "Persona natural"
        return context


class IIVCreateLegalPersonView(IIVCreateCustomerView):
    model = rrgg.models.LegalPerson

    def get_initial(self):
        initial = super().get_initial()
        ruc = rrgg.models.DocumentType.objects.get(code="ruc")
        initial["document_type"] = ruc
        return initial

    def get_success_url(self):
        rrgg.models.CustomerMembership.objects.create(legal_person=self.object)
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:search_vehicle",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.object.membership.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type_customer"] = "Persona jurídica"
        return context


class IIVUpdateNaturalPersonViewSupport(
    rrgg_mixins.RrggBootstrapDisplayMixin, UpdateView
):
    template_name = "rrggweb/quotation/insurance/vehicle/customer_form.html"
    pk_url_kwarg = "natural_person_id"
    model = rrgg.models.NaturalPerson
    fields = "__all__"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["second_surname"].required = False
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Editar contratante"
        return context


class IIVUpdateNaturalPersonStepView(IIVUpdateNaturalPersonViewSupport):
    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:search_vehicle",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.object.membership.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["initial_step"] = 2
        context["final_step"] = 9
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:search_customer",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
            },
        )
        return context


class IIVUpdateNaturalPersonQView(IIVUpdateNaturalPersonViewSupport):
    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:quotation_detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.kwargs["quotation_id"],
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:quotation_detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.kwargs["quotation_id"],
            },
        )
        return context


class IIVUpdateLegalPersonViewSupport(
    rrgg_mixins.RrggBootstrapDisplayMixin, UpdateView
):
    template_name = "rrggweb/quotation/insurance/vehicle/customer_form.html"
    pk_url_kwarg = "legal_person_id"
    model = rrgg.models.LegalPerson
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Editar contratante"
        return context


class IIVUpdateLegalPersonStepView(IIVUpdateLegalPersonViewSupport):
    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:search_vehicle",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.object.membership.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["initial_step"] = 2
        context["final_step"] = 9
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:search_customer",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
            },
        )
        return context


class IIVUpdateLegalPersonQView(IIVUpdateLegalPersonViewSupport):
    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:quotation_detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.kwargs["quotation_id"],
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:quotation_detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.kwargs["quotation_id"],
            },
        )
        return context


# NEW SALE - VEHICLE


class IIVSearchVehicleView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/vehicle_form.html"
    form_class = forms.SearchVehicleForm

    def form_valid(self, form):
        plate = form.cleaned_data["plate"]
        vehicle_exists = rrgg.models.Vehicle.objects.filter(
            plate=plate
        ).exists()
        if vehicle_exists:
            vehicle = rrgg.models.Vehicle.objects.get(plate=plate)
            vehicle_ownership_exists = (
                rrgg.models.VehicleOwnership.objects.filter(
                    vehicle__plate=plate
                ).exists()
            )
            if vehicle_ownership_exists:
                if isinstance(
                    vehicle.ownership.pick, rrgg.models.CustomerMembership
                ):
                    customer = shortcuts.get_object_or_404(
                        rrgg.models.CustomerMembership,
                        id=self.kwargs["customer_id"],
                    )
                    if vehicle.ownership.pick == customer:
                        self.success_url = urls.reverse(
                            (
                                "rrggweb:issuance:insurance:"
                                "vehicle:create_quotation"
                            ),
                            kwargs={
                                "registrar_id": self.kwargs["registrar_id"],
                                "seller_id": self.kwargs["seller_id"],
                                "customer_id": self.kwargs["customer_id"],
                                "vehicle_id": vehicle.id,
                            },
                        )
                    else:
                        form.add_error(
                            "plate",
                            "El contratante no es dueño del vehículo",
                        )
                        return super().form_invalid(form)
                else:
                    # toca evaluar si el propietario registrado es el actual
                    self.success_url = urls.reverse(
                        "rrggweb:issuance:insurance:vehicle:create_quotation",
                        kwargs={
                            "registrar_id": self.kwargs["registrar_id"],
                            "seller_id": self.kwargs["seller_id"],
                            "customer_id": self.kwargs["customer_id"],
                            "vehicle_id": vehicle.id,
                        },
                    )
            else:
                self.success_url = urls.reverse(
                    "rrggweb:issuance:insurance:vehicle:define_owner",
                    kwargs={
                        "registrar_id": self.kwargs["registrar_id"],
                        "seller_id": self.kwargs["seller_id"],
                        "customer_id": self.kwargs["customer_id"],
                        "vehicle_id": vehicle.id,
                    },
                )
        else:
            create_vehicle_url = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:create_vehicle",
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
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Buscar vehículo"
        context["initial_step"] = 3
        context["final_step"] = 9
        context["pretty_style"] = False
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.CustomerMembership, id=self.kwargs["customer_id"]
        )
        # determinar si el contratante es persona natural o jurídica
        customer = shortcuts.get_object_or_404(
            rrgg.models.CustomerMembership, id=self.kwargs["customer_id"]
        )
        person = customer.pick
        if isinstance(person, rrgg.models.NaturalPerson):
            context["previous_page"] = urls.reverse(
                (
                    "rrggweb:issuance:insurance:vehicle:"
                    "update_natural_person_step"
                ),
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                    "natural_person_id": person.id,
                },
            )
        elif isinstance(person, rrgg.models.LegalPerson):
            context["previous_page"] = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:update_legal_person_step",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                    "legal_person_id": person.id,
                },
            )
        else:
            pass

        return context


class IIVCreateVehicleView(rrgg_mixins.RrggBootstrapDisplayMixin, CreateView):
    template_name = "rrggweb/quotation/insurance/vehicle/vehicle_form.html"
    model = rrgg.models.Vehicle
    fields = "__all__"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["has_gps"].required = False
        form.fields["has_endorsee"].required = False
        form.fields["endorsee_bank"].required = False
        return form

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:define_owner",
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
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Registrar vehículo"
        context["initial_step"] = 3
        context["final_step"] = 9
        context["pretty_style"] = True
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.CustomerMembership, id=self.kwargs["customer_id"]
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:search_vehicle",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.kwargs["customer_id"],
            },
        )
        return context


class IIVUpdateVehicleViewSupport(
    rrgg_mixins.RrggBootstrapDisplayMixin, UpdateView
):
    template_name = "rrggweb/quotation/insurance/vehicle/vehicle_form.html"
    model = rrgg.models.Vehicle
    fields = "__all__"
    pk_url_kwarg = "vehicle_id"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["has_gps"].required = False
        form.fields["has_endorsee"].required = False
        form.fields["endorsee_bank"].required = False
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Editar vehículo"
        return context


class IIVUpdateVehicleStepView(IIVUpdateVehicleViewSupport):
    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:define_owner",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.kwargs["customer_id"],
                "vehicle_id": self.object.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["initial_step"] = 3
        context["final_step"] = 9
        context["pretty_style"] = True
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.CustomerMembership, id=self.kwargs["customer_id"]
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:search_vehicle",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.kwargs["customer_id"],
            },
        )
        return context


class IIVUpdateVehicleQView(IIVUpdateVehicleViewSupport):
    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:quotation_detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.kwargs["quotation_id"],
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pretty_style"] = True
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:quotation_detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.kwargs["quotation_id"],
            },
        )
        return context


# NEW SALE - OWNER


class IIVDefineOwnerView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/owner_form.html"
    form_class = forms.DefineOwnerForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["is_owner"].required = False
        return form

    def form_valid(self, form):
        vehicle = shortcuts.get_object_or_404(
            rrgg.models.Vehicle, id=self.kwargs["vehicle_id"]
        )
        vehicle_ownership_exists = rrgg.models.VehicleOwnership.objects.filter(
            vehicle=vehicle
        ).exists()
        if vehicle_ownership_exists:
            vehicle.ownership.delete()
        else:
            pass

        is_customer_owner = form.cleaned_data["is_owner"]
        if is_customer_owner:
            customer = shortcuts.get_object_or_404(
                rrgg.models.CustomerMembership, id=self.kwargs["customer_id"]
            )
            rrgg.models.VehicleOwnership.objects.create(
                customer=customer, vehicle=vehicle
            )
            self.success_url = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:create_quotation",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                    "customer_id": self.kwargs["customer_id"],
                    "vehicle_id": self.kwargs["vehicle_id"],
                },
            )
        else:
            self.success_url = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:search_owner",
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
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Definir propietario"
        context["initial_step"] = 4
        context["final_step"] = 9
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.CustomerMembership, id=self.kwargs["customer_id"]
        )
        context["vehicle"] = shortcuts.get_object_or_404(
            rrgg.models.Vehicle, id=self.kwargs["vehicle_id"]
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:update_vehicle_step",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "vehicle_id": self.kwargs["vehicle_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.kwargs["customer_id"],
            },
        )
        return context


class IIVSearchOwnerView(FormView):
    template_name = "rrggweb/quotation/insurance/vehicle/owner_form.html"
    form_class = forms.SearchPersonForm

    def form_valid(self, form):
        document_number = form.cleaned_data["document_number"]
        if not re.match("^[0-9]+$", document_number):
            form.add_error(
                "document_number",
                "El número de documento debe contener solo números.",
            )
            return super().form_invalid(form)
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
            rrgg.models.VehicleOwnership.objects.create(
                owner=owner, vehicle=vehicle
            )
            self.success_url = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:create_quotation",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                    "customer_id": self.kwargs["customer_id"],
                    "vehicle_id": self.kwargs["vehicle_id"],
                },
            )
        else:
            create_owner_url = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:create_owner",
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
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Buscar propietario"
        context["initial_step"] = 4
        context["final_step"] = 9
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.CustomerMembership, id=self.kwargs["customer_id"]
        )
        context["vehicle"] = shortcuts.get_object_or_404(
            rrgg.models.Vehicle, id=self.kwargs["vehicle_id"]
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:define_owner",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.kwargs["customer_id"],
                "vehicle_id": self.kwargs["vehicle_id"],
            },
        )
        return context


class IIVCreateOwnerView(rrgg_mixins.RrggBootstrapDisplayMixin, CreateView):
    template_name = "rrggweb/quotation/insurance/vehicle/owner_form.html"
    model = rrgg.models.Owner
    fields = "__all__"

    def get_success_url(self):
        vehicle = shortcuts.get_object_or_404(
            rrgg.models.Vehicle, id=self.kwargs["vehicle_id"]
        )
        rrgg.models.VehicleOwnership.objects.create(
            owner=self.object, vehicle=vehicle
        )
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:create_quotation",
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
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Registrar propietario"
        context["body"] = "Formulario del Propietario:"
        context["initial_step"] = 4
        context["final_step"] = 9
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.CustomerMembership, id=self.kwargs["customer_id"]
        )
        context["vehicle"] = shortcuts.get_object_or_404(
            rrgg.models.Vehicle, id=self.kwargs["vehicle_id"]
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:search_owner",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.kwargs["customer_id"],
                "vehicle_id": self.kwargs["vehicle_id"],
            },
        )
        return context


class IIVUpdateOwnerViewSupport(
    rrgg_mixins.RrggBootstrapDisplayMixin, UpdateView
):
    template_name = "rrggweb/quotation/insurance/vehicle/owner_form.html"
    model = rrgg.models.Owner
    fields = "__all__"
    pk_url_kwarg = "owner_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Editar propietario"
        return context


class IIVUpdateOwnerStepView(IIVUpdateOwnerViewSupport):
    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:create_quotation",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.kwargs["customer_id"],
                "vehicle_id": self.kwargs["vehicle_id"],
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["initial_step"] = 4
        context["final_step"] = 9
        context["body"] = "Formulario del Propietario:"
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.CustomerMembership, id=self.kwargs["customer_id"]
        )
        context["vehicle"] = shortcuts.get_object_or_404(
            rrgg.models.Vehicle, id=self.kwargs["vehicle_id"]
        )
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:define_owner",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "customer_id": self.kwargs["customer_id"],
                "vehicle_id": self.kwargs["vehicle_id"],
            },
        )
        return context


class IIVUpdateOwnerQView(IIVUpdateOwnerViewSupport):
    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:quotation_detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.kwargs["quotation_id"],
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:quotation_detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.kwargs["quotation_id"],
            },
        )
        return context


class IIVCreateQuotationView(
    rrgg_mixins.RrggBootstrapDisplayMixin, CreateView
):
    template_name = "rrggweb/quotation/insurance/vehicle/form.html"
    model = rrgg.models.QuotationInsuranceVehicle
    fields = ["insured_amount", "currency"]

    def form_valid(self, form):
        form.instance.risk = rrgg.models.Risk.objects.get(name="Vehicular")
        form.instance.consultant_registrar_id = self.kwargs["registrar_id"]
        form.instance.consultant_seller_id = None
        form.instance.customer_id = self.kwargs["customer_id"]
        form.instance.vehicle_id = self.kwargs["vehicle_id"]
        return super().form_valid(form)

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:create_premium",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.object.id,
                "seller_id": self.kwargs["seller_id"],
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Crear registro vehicular"
        context["initial_step"] = 5
        context["final_step"] = 9
        context["customer"] = shortcuts.get_object_or_404(
            rrgg.models.CustomerMembership, id=self.kwargs["customer_id"]
        )
        context["vehicle"] = shortcuts.get_object_or_404(
            rrgg.models.Vehicle, id=self.kwargs["vehicle_id"]
        )
        context["owner"] = context["vehicle"].ownership

        if isinstance(context["owner"].pick, rrgg.models.Owner):
            context["previous_page"] = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:update_owner_step",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                    "owner_id": context["owner"].owner.id,
                    "customer_id": self.kwargs["customer_id"],
                    "vehicle_id": self.kwargs["vehicle_id"],
                },
            )
        else:
            context["previous_page"] = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:define_owner",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                    "customer_id": self.kwargs["customer_id"],
                    "vehicle_id": self.kwargs["vehicle_id"],
                },
            )
        return context


class IIVUpdateQuotationViewSupport(
    rrgg_mixins.RrggBootstrapDisplayMixin, UpdateView
):
    template_name = "rrggweb/quotation/insurance/vehicle/form.html"
    model = rrgg.models.QuotationInsuranceVehicle
    fields = ["insured_amount", "currency"]
    pk_url_kwarg = "quotation_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Editar registro vehicular"
        return context


class IIVUpdateQuotationStepView(IIVUpdateQuotationViewSupport):
    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:create_premium",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "seller_id": self.kwargs["seller_id"],
                "quotation_id": self.object.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["initial_step"] = 5
        context["final_step"] = 9
        context["customer"] = self.object.customer
        context["vehicle"] = self.object.vehicle
        context["owner"] = context["vehicle"].ownership

        if isinstance(context["owner"].pick, rrgg.models.Owner):
            context["previous_page"] = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:update_owner_step",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                    "customer_id": self.object.customer.id,
                    "vehicle_id": self.object.vehicle.id,
                    "owner_id": context["owner"].owner.id,
                },
            )
        else:
            context["previous_page"] = urls.reverse(
                "rrggweb:issuance:insurance:vehicle:define_owner",
                kwargs={
                    "registrar_id": self.kwargs["registrar_id"],
                    "seller_id": self.kwargs["seller_id"],
                    "customer_id": self.object.customer.id,
                    "vehicle_id": self.object.vehicle.id,
                },
            )
        return context


class IIVUpdateQuotationView(IIVUpdateQuotationViewSupport):
    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:quotation_detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.object.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:quotation_detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.object.id,
            },
        )
        return context


# class IIVQuotationSelectInsuranceFormView(FormView):
#     template_name = "rrggweb/issuance/insurance/vehicle/basic_form.html"
#     form_class = forms.InsuranceVehicleForm

#     def form_valid(self, form: forms.InsuranceVehicleForm):
#         insurance = form.cleaned_data["aseguradoras"]
#         self.success_url = urls.reverse(
#             "rrggweb:issuance:insurance:vehicle:create_premium",
#             kwargs={
#                 "registrar_id": self.kwargs["registrar_id"],
#                 "seller_id": self.kwargs["seller_id"],
#                 "quotation_id": self.kwargs["quotation_id"],
#                 "insurance_id": insurance.id,
#             },
#         )
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = "EMISIÓN VEHICULAR"
#         context["subtitle"] = "Seleccionar aseguradora"
#         context["initial_step"] = 6
#         context["final_step"] = 9
#         context["previous_page"] = urls.reverse(
#             "rrggweb:issuance:insurance:vehicle:update_quotation_step",
#             kwargs={
#                 "registrar_id": self.kwargs["registrar_id"],
#                 "seller_id": self.kwargs["seller_id"],
#                 "quotation_id": self.kwargs["quotation_id"],
#             },
#         )
#         return context


class IIVQuotationPremiumCreateView(
    rrgg_mixins.RrggBootstrapDisplayMixin, CreateView
):
    template_name = "rrggweb/issuance/insurance/vehicle/premium_form.html"
    model = rrgg.models.QuotationInsuranceVehiclePremium
    fields = ["insurance_vehicle_ratio", "amount", "rate"]

    def form_valid(self, form):
        form.instance.quotation_insurance_vehicle_id = self.kwargs[
            "quotation_id"
        ]

        return super().form_valid(form)

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:select_plan_ns",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "premium_id": self.object.id,
                "seller_id": self.kwargs["seller_id"],
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Registrar prima"
        context["initial_step"] = 6
        context["final_step"] = 9
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        quotation = shortcuts.get_object_or_404(
            rrgg.models.QuotationInsuranceVehicle,
            id=self.kwargs["quotation_id"],
        )
        context["risk_selector"] = forms.RiskForm(risk_id=quotation.risk_id)
        context["insured_amount"] = quotation.insured_amount
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:update_quotation_step",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.kwargs["quotation_id"],
                "seller_id": self.kwargs["seller_id"],
            },
        )
        return context


class IIVPremiumsUpdateViewSupport(
    rrgg_mixins.RrggBootstrapDisplayMixin, UpdateView
):
    template_name = "rrggweb/quotation/insurance/vehicle/update_premium.html"
    model = rrgg.models.QuotationInsuranceVehiclePremium
    fields = ["amount", "rate"]
    pk_url_kwarg = "premium_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["insured_amount"] = (
            self.object.quotation_insurance_vehicle.insured_amount
        )
        return context


class IIVPremiumsUpdateStepView(IIVPremiumsUpdateViewSupport):
    fields = ["insurance_vehicle_ratio", "amount", "rate"]

    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:select_plan_ns",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "premium_id": self.object.id,
                "seller_id": self.kwargs["seller_id"],
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Editar Prima de Aseguradora"
        context["initial_step"] = 6
        context["final_step"] = 9
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:update_quotation_step",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.object.quotation_insurance_vehicle.id,
                "seller_id": self.kwargs["seller_id"],
            },
        )
        return context


class IIVPremiumsUpdateQView(IIVPremiumsUpdateViewSupport):
    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:quotation_detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.object.quotation_insurance_vehicle.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Editar Prima de Aseguradora"
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:create_premium",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "quotation_id": self.object.quotation_insurance_vehicle.id,
            },
        )
        return context


class IIVCreateViewSupport(rrgg_mixins.RrggBootstrapDisplayMixin, CreateView):
    template_name = "rrggweb/issuance/insurance/vehicle/form.html"
    model = rrgg.models.IssuanceInsuranceVehicle
    fields = [
        "policy",
        "collection_document",
        "issuance_date",
        "initial_validity",
        "final_validity",
        "plan_commission_percentage",
        "payment_method",
    ]

    def get_initial(self):
        initial = super().get_initial()
        plan = shortcuts.get_object_or_404(
            rrgg.models.InsurancePlan, id=self.kwargs["plan_id"]
        )
        kcs_commission_percentage = round(plan.commission * 100, 1)
        initial["plan_commission_percentage"] = kcs_commission_percentage
        return initial

    def form_valid(self, form):
        form.instance.consultant_registrar_id = self.kwargs["registrar_id"]
        form.instance.consultant_seller_id = self.kwargs["seller_id"]
        form.instance.insurance_plan_id = self.kwargs["plan_id"]
        form.instance.quotation_vehicle_premium_id = self.kwargs["premium_id"]
        raw_percentage = form.cleaned_data["plan_commission_percentage"]
        form.instance.plan_commission_percentage = raw_percentage / 100
        seller = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        form.instance.seller_commission_percentage = (
            seller.commission_rate.new_sale
        )
        # validate expiration date
        quotation_premium = shortcuts.get_object_or_404(
            rrgg.models.QuotationInsuranceVehiclePremium,
            id=self.kwargs["premium_id"],
        )
        if quotation_premium.quotation_insurance_vehicle.expired:
            messages.warning(self.request, "Esta cotización ya expiró")
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Crear emisión"
        context["premium"] = shortcuts.get_object_or_404(
            rrgg.models.QuotationInsuranceVehiclePremium,
            id=self.kwargs["premium_id"],
        )
        context["seller"] = shortcuts.get_object_or_404(
            rrgg.models.Consultant, id=self.kwargs["seller_id"]
        )
        context["ratio"] = context["premium"].insurance_vehicle_ratio
        context["insurance_plan"] = shortcuts.get_object_or_404(
            rrgg.models.InsurancePlan, id=self.kwargs["plan_id"]
        )
        context["quotation"] = context["premium"].quotation_insurance_vehicle
        context["customer"] = context["quotation"].customer
        context["vehicle"] = context["quotation"].vehicle
        context["owner"] = context["vehicle"].ownership
        return context


class IIVCreateStepQView(IIVCreateViewSupport):
    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:create_document_q",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "issuance_id": self.object.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["initial_step"] = 3
        context["final_step"] = 4
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:select_plan_q",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "premium_id": self.kwargs["premium_id"],
                "seller_id": self.kwargs["seller_id"],
            },
        )
        return context


class IIVCreateStepNSView(IIVCreateViewSupport):
    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:create_document_ns",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "issuance_id": self.object.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["initial_step"] = 8
        context["final_step"] = 9
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:select_plan_ns",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "premium_id": self.kwargs["premium_id"],
                "seller_id": self.kwargs["seller_id"],
            },
        )
        return context


class IIVUpdateIssuanceSupport(
    rrgg_mixins.RrggBootstrapDisplayMixin, UpdateView
):
    template_name = "rrggweb/issuance/insurance/vehicle/form.html"
    model = rrgg.models.IssuanceInsuranceVehicle
    fields = [
        "policy",
        "collection_document",
        "issuance_date",
        "initial_validity",
        "final_validity",
        "plan_commission_percentage",
        "payment_method",
    ]
    pk_url_kwarg = "issuance_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Editar Emisión"
        return context


class IIVUpdateIssuanceStepQView(IIVUpdateIssuanceSupport):
    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:create_document_q",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "issuance_id": self.object.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["initial_step"] = 3
        context["final_step"] = 4
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:select_plan_q",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "premium_id": self.object.quotation_vehicle_premium.id,
                "seller_id": self.object.consultant_seller.id,
            },
        )
        return context


class IIVUpdateIssuanceStepNSView(IIVUpdateIssuanceSupport):
    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:create_document_ns",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "issuance_id": self.object.id,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["initial_step"] = 8
        context["final_step"] = 9
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:select_plan_ns",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "premium_id": self.object.quotation_vehicle_premium.id,
                "seller_id": self.object.consultant_seller.id,
            },
        )
        return context


class IIVAddDocumentSupportCreateView(
    rrgg_mixins.RrggBootstrapDisplayMixin, CreateView
):
    template_name = "rrggweb/issuance/insurance/vehicle/document_form.html"
    model = rrgg.models.IssuanceInsuranceVehicleDocument
    fields = ["issuance", "file"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Subir documentos"
        context["type"] = "create"
        context["documents"] = self.model.objects.filter(
            issuance_id=self.kwargs["issuance_id"]
        )
        context["finish"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "issuance_id": self.kwargs["issuance_id"],
            },
        )
        return context


class IIVAddDocumentQCreateView(IIVAddDocumentSupportCreateView):
    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:create_document_q",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "issuance_id": self.kwargs["issuance_id"],
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["initial_step"] = 4
        context["final_step"] = 4
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:update_step_q",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "issuance_id": self.kwargs["issuance_id"],
            },
        )
        return context


class IIVAddDocumentNSCreateView(IIVAddDocumentSupportCreateView):
    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:create_document_ns",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "issuance_id": self.kwargs["issuance_id"],
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["initial_step"] = 9
        context["final_step"] = 9
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:update_step_ns",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "issuance_id": self.kwargs["issuance_id"],
            },
        )
        return context


class IIVDeleteDocumentSupportView(DeleteView):
    template_name = "rrggweb/issuance/insurance/vehicle/document_form.html"
    model = rrgg.models.IssuanceInsuranceVehicleDocument
    pk_url_kwarg = "document_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Eliminar documento"
        context["type"] = "delete"
        return context


class IIVDeleteDocumentQView(IIVDeleteDocumentSupportView):
    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:create_document_q",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "issuance_id": self.kwargs["issuance_id"],
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["initial_step"] = 4
        context["final_step"] = 4
        context["return"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:create_document_q",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "issuance_id": self.kwargs["issuance_id"],
            },
        )
        return context


class IIVDeleteDocumentNSView(IIVDeleteDocumentSupportView):
    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:create_document_ns",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "issuance_id": self.kwargs["issuance_id"],
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["initial_step"] = 9
        context["final_step"] = 9
        context["return"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:create_document_ns",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "issuance_id": self.kwargs["issuance_id"],
            },
        )
        return context


class IIVUpdateIssuanceView(IIVUpdateIssuanceSupport):
    def get_success_url(self):
        return urls.reverse(
            "rrggweb:issuance:insurance:vehicle:list",
            kwargs={"registrar_id": self.kwargs["registrar_id"]},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["step"] = False
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:list",
            kwargs={"registrar_id": self.kwargs["registrar_id"]},
        )
        return context


class IIVUpdateStatusFormView(FormView):
    template_name = "rrggweb/issuance/insurance/vehicle/basic_form.html"
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EMISIÓN VEHICULAR"
        context["subtitle"] = "Gestionar estado de emisión"
        context["previous_page"] = urls.reverse(
            "rrggweb:issuance:insurance:vehicle:detail",
            kwargs={
                "registrar_id": self.kwargs["registrar_id"],
                "issuance_id": self.kwargs["issuance_id"],
            },
        )
        return context


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
