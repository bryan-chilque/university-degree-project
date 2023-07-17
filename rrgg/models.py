from django.contrib.auth import get_user_model
from django.db import models


class Customer(models.Model):
    give_name = models.CharField(max_length=64)
    first_surname = models.CharField(max_length=64)
    second_surname = models.CharField(max_length=64, blank=True)
    document_number = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.give_name + " " + self.first_surname


class Vehicle(models.Model):
    brand = models.CharField(max_length=64)
    vehicle_model = models.CharField(max_length=64)
    property_number = models.CharField(max_length=64, unique=True)
    fabrication_year = models.PositiveIntegerField(default=0)

    customer = models.ForeignKey(
        Customer,
        related_name="vehicles",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"{self.brand} {self.vehicle_model} {self.fabrication_year}"


class Consultant(models.Model):
    give_name = models.CharField(max_length=64)
    first_surname = models.CharField(max_length=64)
    second_surname = models.CharField(max_length=64, blank=True)
    document_number = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.give_name + " " + self.first_surname


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


class InsuranceVehicle(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    def last_price(self):
        return self.prices.order_by("-created").first()


class InsuranceVehiclePrice(models.Model):
    business_premium = models.PositiveIntegerField()
    emission_right = models.PositiveIntegerField()
    tax = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True, unique=True)
    insurance_vehicle = models.ForeignKey(
        InsuranceVehicle, related_name="prices", on_delete=models.PROTECT
    )

    @property
    def total(self):
        return self.business_premium + self.emission_right + self.tax

    def __str__(self) -> str:
        return (
            f"bp={self.business_premium} er={self.emission_right}"
            f"tax={self.tax} total={self.total}"
        )


class QuotationInsuranceVehicle(models.Model):
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
    insurance_vehicle_price = models.ForeignKey(
        InsuranceVehiclePrice,
        related_name="quotation_insurance_vehicle",
        on_delete=models.PROTECT,
    )
    created = models.DateTimeField(auto_now_add=True)
    observations = models.TextField(max_length=512, blank=True)

    def __str__(self):
        return (
            f"Consultant={self.consultant} iv={self.insurance_vehicle_price}"
            f" Customer={self.vehicle.customer} ({self.created})"
        )
