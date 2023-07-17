from django import forms


class SearchByDocumentNumberForm(forms.Form):
    document_number = forms.CharField(
        max_length=32,
        label="Número de documento",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
