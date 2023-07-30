from django import forms
from django.contrib.auth import forms as forms_auth
from django.utils.translation import gettext as _


class SearchByDocumentNumberForm(forms.Form):
    document_number = forms.CharField(
        max_length=32,
        label=_("document number"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )


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
