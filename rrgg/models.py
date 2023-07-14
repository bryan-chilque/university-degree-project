from django.db import models


class Customer(models.Model):
    give_name = models.CharField(max_length=64)
    first_surname = models.CharField(max_length=64)
    second_surname = models.CharField(max_length=64, null=True)
    document_number = models.CharField(max_length=32)

    def __str__(self):
        return self.give_name + " " + self.first_surname


class Vehicle(models.Model):
    brand = models.CharField(max_length=64)
    vehicle_model = models.CharField(max_length=64)
    property_number = models.CharField(max_length=64)
    fabrication_year = models.PositiveIntegerField(default=0)

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
    give_name = models.CharField(max_length=64)
    first_surname = models.CharField(max_length=64)
    second_surname = models.CharField(max_length=64)
    document_number = models.CharField(max_length=32)

    def __str__(self):
        return self.give_name + self.first_surname


class InsuranceVehicle(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    def last_price(self):
        return self.prices.order_by("-created").first()


class InsuranceVehiclePrice(models.Model):
    business_premium = models.PositiveIntegerField()
    emission_right = models.PositiveIntegerField()
    tax = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    insurance_vehicle = models.ForeignKey(
        InsuranceVehicle, related_name="prices", on_delete=models.PROTECT
    )

    @property
    def total(self):
        return self.business_premium + self.emission_right + self.tax

    def __str__(self) -> str:
        return f"business_premium={self.business_premium}"


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
    created = models.DateTimeField(auto_now_add=True)
    observations = models.TextField(max_length=512)

    # TODO: Pensar que puede devolver
    def __str__(self):
        return self.customer.give_name + " " + self.customer.first_surname
