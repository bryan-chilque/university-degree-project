from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)
from django.db import models


class Customer(models.Model):
    give_name = models.CharField(max_length=64, default="")
    first_surname = models.CharField(max_length=64, default="")
    second_surname = models.CharField(max_length=64, default="")
    dni = models.CharField(
        max_length=8,
        default="",
        validators=[
            MinLengthValidator(8),
            MaxLengthValidator(8),
            RegexValidator(r"^\d+$"),
        ],
    )

    def __str__(self):
        return self.give_name + " " + self.first_surname


class Vehicle(models.Model):
    brand = models.CharField(max_length=64, default="")
    vehicle_model = models.CharField(max_length=64, default="")
    property_number = models.CharField(max_length=64, default="")
    fabrication_year = models.PositiveIntegerField(
        default=0, validators=[MinLengthValidator(4), MaxLengthValidator(4)]
    )
    use = models.CharField(max_length=128, default="")

    customer = models.ForeignKey(
        Customer,
        related_name="vehicles",
        on_delete=models.PROTECT,
        null=False,
    )

    def __str__(self):
        return (
            self.brand + " " + self.vehicle_model + " " + self.fabrication_year
        )


class Consultant(models.Model):
    give_name = models.CharField(max_length=64, default="")
    first_surname = models.CharField(max_length=64, default="")
    second_surname = models.CharField(max_length=64, default="")
    dni = models.CharField(
        max_length=8,
        default="",
        validators=[
            MinLengthValidator(8),
            MaxLengthValidator(8),
            RegexValidator(r"^\d+$"),
        ],
    )

    def __str__(self):
        return self.give_name + self.first_surname


class InsuranceVehicle(models.Model):
    name = models.CharField(max_length=64, default="")

    def __str__(self):
        return self.name


class InsuranceVehiclePrice(models.Model):
    name = models.CharField(max_length=64, default="")
    business_premium = models.PositiveIntegerField()
    emission_right = models.PositiveIntegerField()
    igv = models.PositiveIntegerField()
    insurance_vehicle = models.ForeignKey(
        InsuranceVehicle,
        related_name="insurance_vehicle_prices",
        on_delete=models.PROTECT,
        null=False,
    )

    @property
    def prima_total(self):
        return self.business_premium + self.emission_right + self.igv

    def __str__(self):
        return self.name


class InsuranceVehicleQuotation(models.Model):
    vehicle = models.OneToOneField(
        Vehicle,
        related_name="insurance_vehicle_quotation",
        on_delete=models.PROTECT,
        null=False,
    )
    consultant = models.OneToOneField(
        Consultant,
        related_name="insurance_vehicle_quotation",
        on_delete=models.PROTECT,
        null=True,
    )
    insurance_vehicle_price = models.OneToOneField(
        InsuranceVehiclePrice,
        related_name="insurance_vehicle_quotation",
        on_delete=models.PROTECT,
        null=False,
    )
    date = models.DateField(null=False)
    hour = models.TimeField(null=False)
    observations = models.CharField(max_length=128, default="")

    # TODO: Pensar que puede devolver
    def __str__(self):
        return self.customer.give_name + " " + self.customer.first_surname
