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
    name = models.CharField(max_length=64, unique=True)

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


# Issuance


class Issuance(models.Model):
    policy_number = models.CharField(max_length=64, unique=True)  # Numero de poliza
    collection_document = models.CharField(
        max_length=64, unique=True
    )  # Documento de cobranza
    broadcast_date = models.DateTimeField()  # Fecha de emision
    start_date = models.DateTimeField()  # Fecha de inicio
    end_date = models.DateTimeField()  # Fecha de fin
    amount_insured = models.PositiveIntegerField()  # Monto asegurado
    net_premium = models.PositiveIntegerField()  # Prima neta
    emission_right = models.PositiveIntegerField(default=3)  # Derecho de emision

    @property
    def rate(self):  # Tasa
        return "{:.2f}%".format(self.net_bonus / self.amount_insured * 100)

    @property
    def commercial_premium(self):  # Prima comercial
        return self.emission_right * self.net_bonus

    @property
    def total_premium(self): # Prima total
        return self.commercial_premium * 1.18

    #TODO: Agregar campos de la tabla de emision

    quotation_insurance_vehicle = models.ForeignKey(
        QuotationInsuranceVehicle,
        related_name="issuance",
        on_delete=models.PROTECT,
    )
    created = models.DateTimeField(auto_now_add=True)
    observations = models.TextField(max_length=512, blank=True)
