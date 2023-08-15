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


class SellerForm(forms.Form):
    sellers = forms.ModelChoiceField(
        label=_("sellers"),
        queryset=rrgg.models.Consultant.objects.exclude(
            role__name="Administrativos"
        ),
        widget=forms.Select(attrs={"class": "form-select"}),
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
        label=_("is contractor or insured?"),
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "type": "checkbox"}
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
