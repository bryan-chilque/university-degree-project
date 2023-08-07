from django import forms
from django.contrib.auth import forms as forms_auth
from django.utils.translation import gettext as _


class LoginAuthenticationForm(forms_auth.AuthenticationForm):
    username = forms.CharField(
        max_length=32,
        label="Usuario",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        max_length=32,
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
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
        label=_("is owner?"),
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "type": "checkbox"}
        ),
    )
