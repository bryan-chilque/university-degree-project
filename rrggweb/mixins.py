from django import forms
from django.db import models


class RrggBootstrapDisplayMixin:
    def get_form_class(self):
        return forms.modelform_factory(
            self.model,
            fields=self.fields,
            formfield_callback=self.__formfield_callback,
        )

    @staticmethod
    def __formfield_callback(model_field):
        if isinstance(model_field, models.CharField):
            return forms.CharField(
                max_length=model_field.max_length,
                widget=forms.TextInput(attrs={"class": "form-control"}),
            )
        elif isinstance(model_field, models.PositiveIntegerField):
            return forms.IntegerField(
                widget=forms.NumberInput(attrs={"class": "form-control"})
            )
        else:
            return model_field.formfield()
