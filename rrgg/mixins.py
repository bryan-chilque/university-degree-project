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
        elif isinstance(model_field, models.ForeignKey):
            return forms.ModelChoiceField(
                queryset=model_field.related_model.objects.all(),
                widget=forms.Select(attrs={"class": "form-select"}),
            )
        elif isinstance(model_field, models.PositiveIntegerField):
            return forms.IntegerField(
                widget=forms.NumberInput(attrs={"class": "form-control"})
            )
        else:
            print(model_field)
            print(type(model_field))
            if model_field.formfield() is not None:
                print(type(model_field.formfield().widget))
            return model_field.formfield()
