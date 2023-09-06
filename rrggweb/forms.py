from django import forms
from django.contrib.auth import forms as forms_auth
from django.utils.translation import gettext as _

import rrgg.models


class LoginAuthenticationForm(forms_auth.AuthenticationForm):
    username = forms.CharField(
        max_length=32,
        label="Usuario",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingresa tu usuario",
            }
        ),
        label_suffix="",
    )
    password = forms.CharField(
        max_length=32,
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingresa tu contraseña",
            }
        ),
        label_suffix="",
    )


class RoleForm(forms.Form):
    def __init__(self, role_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        roles = rrgg.models.Role.objects.all()
        self.fields["roles"] = forms.ModelChoiceField(
            queryset=roles,
            empty_label=None,
            widget=forms.Select(attrs={"class": "form-select mb-2"}),
        )

        if role_id:
            try:
                selected_role = rrgg.models.Role.objects.get(pk=role_id)
                self.fields["roles"].initial = selected_role
            except rrgg.models.Role.DoesNotExist:
                pass


class SellerForm(forms.Form):
    def __init__(self, role_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sellers = rrgg.models.Consultant.objects.all()
        self.fields["asesores"] = forms.ModelChoiceField(
            queryset=sellers,
            empty_label=None,
            widget=forms.Select(attrs={"class": "form-select mb-2"}),
        )

        if role_id:
            self.fields["asesores"].queryset = (
                rrgg.models.Consultant.objects.filter(role_id=role_id)
            )


class SelectCustomerForm(forms.Form):
    TYPE_CHOICES = (
        ("persona_natural", "Persona natural"),
        ("persona_jurídica", "Persona jurídica"),
    )

    type_customer = forms.ChoiceField(
        choices=TYPE_CHOICES,
        label=_("type customer"),
        widget=forms.RadioSelect,
    )


class SearchPersonForm(forms.Form):
    document_number = forms.CharField(
        max_length=32,
        label=_("document number"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )


class SearchVehicleForm(forms.Form):
    plate = forms.CharField(
        max_length=32,
        label=_("plate"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )


class DefineOwnerForm(forms.Form):
    is_owner = forms.BooleanField(
        label=_("does the contractor own the vehicle?"),
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check",
                "type": "checkbox",
                "for": "is_owner",
            }
        ),
    )


class CurrencyForm(forms.Form):
    def __init__(self, currency_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        currencies = rrgg.models.Currency.objects.all()
        self.fields["currencies"] = forms.ModelChoiceField(
            queryset=currencies,
            empty_label=None,
            widget=forms.Select(attrs={"class": "form-select mb-2"}),
        )

        if currency_id:
            try:
                selected_currency = rrgg.models.Currency.objects.get(
                    pk=currency_id
                )
                self.fields["currencies"].initial = selected_currency
            except rrgg.models.Currency.DoesNotExist:
                pass


class RiskForm(forms.Form):
    def __init__(self, risk_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        risks = rrgg.models.Risk.objects.all()
        self.fields["riesgos"] = forms.ModelChoiceField(
            queryset=risks,
            empty_label=None,
            widget=forms.Select(attrs={"class": "form-select mb-2"}),
        )

        if risk_id:
            try:
                selected_risk = rrgg.models.Risk.objects.get(pk=risk_id)
                self.fields["riesgos"].initial = selected_risk
            except rrgg.models.Risk.DoesNotExist:
                pass


class SelectVehicleRegistrationTypeForm(forms.Form):
    TYPE_CHOICES = (
        ("new_sale", "venta nueva"),
        ("renewal", "renovación"),
    )

    vehicle_registration_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        label=_("vehicle registration type"),
        widget=forms.RadioSelect,
    )


class InsuranceVehicleForm(forms.Form):
    def __init__(self, iv_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        insurance_vehicle = rrgg.models.InsuranceVehicle.objects.all()
        self.fields["aseguradoras"] = forms.ModelChoiceField(
            queryset=insurance_vehicle,
            empty_label=None,
            widget=forms.Select(attrs={"class": "form-select mb-2"}),
        )

        if iv_id:
            try:
                selected_iv = rrgg.models.InsuranceVehicle.objects.get(
                    pk=iv_id
                )
                self.fields["aseguradoras"].initial = selected_iv
            except rrgg.models.InsuranceVehicle.DoesNotExist:
                pass


class DefineNewSaleForm(forms.Form):
    has_quote = forms.BooleanField(
        label=_("new sale has a previous quote?"),
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check",
                "type": "checkbox",
                "for": "has_quote",
            }
        ),
    )


class InsurancePlanForm(forms.Form):
    def __init__(self, riv_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        plans = rrgg.models.InsurancePlan.objects.all()
        self.fields["planes de seguro"] = forms.ModelChoiceField(
            queryset=plans,
            empty_label=None,
            widget=forms.Select(attrs={"class": "form-select mb-2"}),
        )

        if riv_id:
            self.fields["planes de seguro"].queryset = (
                rrgg.models.InsurancePlan.objects.filter(
                    risk_insurance_vehicle_id=riv_id
                )
            )


class IssuanceStatusForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=rrgg.models.IssuanceInsuranceStatus.objects.all()
    )
    comment = forms.CharField(
        max_length=256,
        label=_("comment"),
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )
