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
                rol_preseleccionado = rrgg.models.Role.objects.get(pk=role_id)
                self.fields["roles"].initial = rol_preseleccionado
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
        label=_("Is the insured the same as the contracting party?"),
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check",
                "type": "checkbox",
                "for": "is_owner",
            }
        ),
    )


class IssuanceTypeForm(forms.Form):
    TYPE_CHOICES = (
        ("policy", "Póliza vehicular"),
        ("endorsement", "Endoso con movimiento de prima"),
    )

    tipo = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.RadioSelect)


class IssuanceStatusForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=rrgg.models.IssuanceInsuranceStatus.objects.all()
    )
    comment = forms.CharField(
        max_length=256,
        label=_("comment"),
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )
