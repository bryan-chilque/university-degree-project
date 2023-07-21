from django.contrib.auth import get_user_model
from django.db import models


class Customer(models.Model):
    given_name = models.CharField(max_length=64)
    first_surname = models.CharField(max_length=64)
    second_surname = models.CharField(max_length=64, blank=True)
    document_number = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.given_name + " " + self.first_surname


class UseType(models.Model):
    name = models.CharField(max_length=64, unique=True, null=True)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    brand = models.CharField(max_length=64)
    vehicle_model = models.CharField(max_length=64)
    plate = models.CharField(max_length=64, unique=True)
    fabrication_year = models.PositiveIntegerField(default=0)
    engine = models.CharField(max_length=64, default="")
    chassis = models.CharField(max_length=64, default="")

    use_type = models.ForeignKey(
        UseType,
        related_name="use_type",
        on_delete=models.PROTECT,
        null=True,
    )

    customer = models.ForeignKey(
        Customer,
        related_name="vehicles",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"{self.brand} {self.vehicle_model} {self.fabrication_year}"


class Consultant(models.Model):
    given_name = models.CharField(max_length=64)
    first_surname = models.CharField(max_length=64)
    second_surname = models.CharField(max_length=64, blank=True)
    document_number = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.given_name + " " + self.first_surname


class ConsultantMembership(models.Model):
    consultant = models.ForeignKey(
        Consultant, on_delete=models.PROTECT, related_name="membership"
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name="consultant_membership",
    )

    def __str__(self):
        return f"consultant={self.consultant}, user={self.user}"


# cotización de seguro vehicular
class QuotationInsuranceVehicle(models.Model):
    # suma asegurada
    insured_amount = models.PositiveIntegerField(default=0, null=True)
    vehicle = models.ForeignKey(
        Vehicle,
        related_name="quotation_insurance_vehicle",
        on_delete=models.PROTECT,
    )
    consultant = models.ForeignKey(
        Consultant,
        related_name="quotation_insurance_vehicle",
        on_delete=models.PROTECT,
    )
    created = models.DateTimeField(auto_now_add=True)


# aseguradora
class InsuranceVehicle(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"name={self.name}"

    def last_ratio(self):
        return self.ratio.order_by("-created").first()


# relación precio - aseguradora
class InsuranceVehicleRatio(models.Model):
    # derecho de emisión
    emission_right = models.PositiveIntegerField()
    # impuesto (igv)
    tax = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True, unique=True)
    insurance_vehicle = models.ForeignKey(
        InsuranceVehicle, related_name="ratio", on_delete=models.PROTECT
    )


class InsuranceVehiclePremium(models.Model):
    # prima neta o comercial
    business_premium = models.PositiveIntegerField()
    insurance_vehicle_ratio = models.ForeignKey(
        InsuranceVehicleRatio,
        related_name="insurance_vehicle_premium",
        on_delete=models.PROTECT,
    )
    quotation_insurance_vehicle = models.ForeignKey(
        QuotationInsuranceVehicle,
        related_name="insurance_vehicle_premiums",
        on_delete=models.PROTECT,
    )
    created = models.DateTimeField(auto_now_add=True, unique=True)

    @property
    def total(self):
        return (
            self.business_premium
            + self.insurance_vehicle_ratio.emission_right
            + self.insurance_vehicle_ratio.tax
        )

    def __str__(self) -> str:
        return (
            f"bp={self.business_premium}"
            f"er={self.insurance_vehicle_ratio.emission_right}"
            f"tax={self.insurance_vehicle_ratio.tax} total={self.total}"
        )
