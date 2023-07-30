from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Customer(models.Model):
    given_name = models.CharField(max_length=64)
    first_surname = models.CharField(max_length=64)
    second_surname = models.CharField(max_length=64, blank=True)
    document_number = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f"{self.given_name} {self.first_surname}"


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
        return f"{self.brand} {self.vehicle_model} {self.plate}"


class Consultant(models.Model):
    given_name = models.CharField(max_length=64)
    first_surname = models.CharField(max_length=64)
    second_surname = models.CharField(max_length=64, blank=True)
    document_number = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f"{self.given_name} {self.first_surname}"


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
    insured_amount = models.PositiveIntegerField(null=True)
    vehicle = models.ForeignKey(
        Vehicle,
        related_name="quotation_insurance_vehicles",
        on_delete=models.PROTECT,
    )
    consultant = models.ForeignKey(
        Consultant,
        related_name="quotation_insurance_vehicles",
        on_delete=models.PROTECT,
    )
    created = models.DateTimeField(auto_now_add=True)

    @property
    def expired(self):
        return timezone.now() - self.created > timezone.timedelta(days=15)

    def __str__(self):
        return f"insured_amount={self.insured_amount}, vehicle={self.vehicle}"


# aseguradora
class InsuranceVehicle(models.Model):
    name = models.CharField(max_length=64, unique=True)
    logo = models.ImageField(
        upload_to="insurance_vehicle_images/", blank=True, null=True
    )

    def __str__(self):
        return self.name

    @property
    def last_ratio(self):
        return self.ratios.order_by("-created").first()


# relación precio - aseguradora
class InsuranceVehicleRatio(models.Model):
    # derecho de emisión
    emission_right = models.DecimalField(
        decimal_places=2, max_digits=10, null=False
    )
    # impuesto (igv)
    tax = models.DecimalField(decimal_places=2, max_digits=10, null=False)
    # cuotas
    fee = models.PositiveIntegerField(null=True)
    # débito automático
    direct_debit = models.PositiveIntegerField(null=True)

    created = models.DateTimeField(auto_now_add=True, unique=True)
    insurance_vehicle = models.ForeignKey(
        InsuranceVehicle, related_name="ratios", on_delete=models.PROTECT
    )

    def __str__(self):
        return (
            f"er={self.emission_right},"
            f" tax={self.tax},"
            f" fee={self.fee},"
            f" insurance_vehicle={self.insurance_vehicle}"
        )


class QuotationInsuranceVehiclePremium(models.Model):
    # prima neta
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    insurance_vehicle_ratio = models.ForeignKey(
        InsuranceVehicleRatio,
        related_name="quotation_insurance_vehicle_premiums",
        on_delete=models.PROTECT,
    )
    quotation_insurance_vehicle = models.ForeignKey(
        QuotationInsuranceVehicle,
        related_name="premiums",
        on_delete=models.PROTECT,
    )
    created = models.DateTimeField(auto_now_add=True, unique=True)

    @property
    def emission_right(self):
        return round(
            self.amount * self.insurance_vehicle_ratio.emission_right, 2
        )

    @property
    def tax(self):
        value = self.amount + self.emission_right
        return round(value * self.insurance_vehicle_ratio.tax, 2)

    # tasa
    @property
    def rate(self):
        q = self.quotation_insurance_vehicle
        return round(self.amount / q.insured_amount, 2)

    # prima comercial
    @property
    def commercial_premium(self):
        q = self.insurance_vehicle_ratio
        return round(self.amount + q.emission_right, 2)

    # prima total
    @property
    def total(self):
        return self.amount + self.emission_right + self.tax

    # fee
    @property
    def fee(self):
        q = self.insurance_vehicle_ratio
        return round(self.total / q.fee, 2)

    # direct_debit
    @property
    def direct_debit(self):
        q = self.insurance_vehicle_ratio
        return round(self.total / q.direct_debit, 2)

    def __str__(self) -> str:
        return (
            f"premium={self.amount},"
            f" er={self.emission_right},"
            f" tax={self.tax} total={self.total}"
        )


# Issuance
class IssuanceInsuranceVehicle(models.Model):
    # numero de póliza
    policy = models.CharField(max_length=64)
    # documento de cobranza
    collection_document = models.CharField(max_length=64)
    # fecha de emisión de la póliza
    issuance_date = models.DateTimeField(null=True)
    # fecha de vigencia final
    initial_validity = models.DateTimeField()
    # fecha de vigencia inicio
    final_validity = models.DateTimeField()

    quotation_vehicle_premium = models.ForeignKey(
        QuotationInsuranceVehiclePremium,
        related_name="issuance",
        on_delete=models.PROTECT,
    )

    created = models.DateTimeField(auto_now_add=True)
