from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Role(models.Model):
    name = models.CharField(_("name"), max_length=64, unique=True)

    class Meta:
        verbose_name = _("role")
        verbose_name_plural = _("roles")

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(_("name"), max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("area")
        verbose_name_plural = _("areas")


class Consultant(models.Model):
    given_name = models.CharField(_("given name"), max_length=64)
    first_surname = models.CharField(_("first surname"), max_length=64)
    second_surname = models.CharField(
        _("second surname"), max_length=64, blank=True
    )
    role = models.ForeignKey(
        Role,
        related_name="consultant",
        verbose_name=_("role"),
        on_delete=models.PROTECT,
    )
    area = models.ManyToManyField(
        "Area", related_name="consultant", verbose_name=_("area")
    )

    class Meta:
        verbose_name = _("consultant")
        verbose_name_plural = _("consultants")

    def __str__(self):
        return f"{self.given_name} {self.first_surname}"


class ConsultantRate(models.Model):
    new_sale = models.DecimalField(
        _("new sale"), decimal_places=2, max_digits=10
    )
    renewal = models.DecimalField(
        _("renewal"), decimal_places=2, max_digits=10
    )
    consultant = models.OneToOneField(
        Consultant,
        related_name="commission_rate",
        verbose_name=_("consultant"),
        on_delete=models.PROTECT,
    )
    created = models.DateTimeField(auto_now_add=True)


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


class DocumentType(models.Model):
    code = models.CharField(max_length=16)
    name = models.CharField(max_length=128)
    min_length = models.IntegerField(default=0)
    max_length = models.IntegerField(default=0)

    class Meta:
        verbose_name = _("document type")

    def __str__(self):
        return self.code


class Person(models.Model):
    phone_number = models.CharField(_("phone number"), max_length=32)
    email = models.EmailField(_("email"), max_length=64)
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.PROTECT,
        verbose_name=_("document type"),
    )
    document_number = models.CharField(
        _("document number"), max_length=32, unique=True
    )

    class Meta:
        abstract = True


class NaturalPerson(Person):
    given_name = models.CharField(_("given name"), max_length=64)
    first_surname = models.CharField(_("first surname"), max_length=64)
    second_surname = models.CharField(
        _("second surname"), max_length=64, blank=True
    )
    birthdate = models.DateField(_("birthdate"))

    def __str__(self):
        return f"{self.given_name} {self.first_surname}"


class LegalPerson(Person):
    # nombre comercial
    business_name = models.CharField(
        _("business name"), max_length=64, unique=True
    )
    # razón social
    registered_name = models.CharField(_("registered name"), max_length=64)
    general_manager = models.CharField(_("general manager"), max_length=64)
    anniversary_date = models.DateField(_("anniversary date"))

    def __str__(self):
        return self.business_name


class CustomerMembership(models.Model):
    natural_person = models.OneToOneField(
        NaturalPerson,
        on_delete=models.PROTECT,
        null=True,
        related_name="membership",
    )
    legal_person = models.OneToOneField(
        LegalPerson,
        on_delete=models.PROTECT,
        null=True,
        related_name="membership",
    )

    @property
    def pick(self):
        return self.natural_person or self.legal_person

    def save(self, *args, **kwargs):
        if self.natural_person and self.legal_person:
            raise ValueError(
                "El cliente no puede ser persona natural y jurídica al"
                " mismo tiempo."
            )
        super().save(*args, **kwargs)

    def __str__(self):
        if self.natural_person:
            return f"{self.natural_person}"
        elif self.legal_person:
            return f"{self.legal_person}"


class Owner(models.Model):
    given_name = models.CharField(_("given name"), max_length=64)
    first_surname = models.CharField(_("first surname"), max_length=64)
    second_surname = models.CharField(
        _("second surname"), max_length=64, blank=True
    )
    document_number = models.CharField(
        _("document number"), max_length=32, unique=True
    )
    birthdate = models.DateField(_("birthdate"))
    phone_number = models.CharField(_("phone number"), max_length=32)
    email = models.EmailField(_("email"), max_length=64)

    def __str__(self):
        return f"{self.given_name} {self.first_surname}"


class UseType(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Bank(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    brand = models.CharField(_("brand"), max_length=64)
    vehicle_model = models.CharField(_("model"), max_length=64)
    plate = models.CharField(_("plate"), max_length=64, unique=True)
    fabrication_year = models.PositiveIntegerField(_("fabrication year"))
    engine = models.CharField(_("engine number"), max_length=64)
    chassis = models.CharField(_("chassis number"), max_length=64)
    seat_number = models.PositiveIntegerField(_("seat number"))
    # vehículo gps
    has_gps = models.BooleanField(_("has gps?"), default=False)
    # vehículo tiene endoso
    has_endorsee = models.BooleanField(_("has endorsee?"), default=False)
    endorsee_bank = models.ForeignKey(
        Bank,
        verbose_name=_("endorsee bank"),
        on_delete=models.PROTECT,
        null=True,
    )
    use_type = models.ForeignKey(
        UseType,
        related_name="use_type",
        verbose_name=_("usage"),
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = _("vehicle")
        verbose_name_plural = _("vehicles")

    def save(self, *args, **kwargs):
        if not self.has_endorsee:
            self.endorsee_bank = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.vehicle_model} {self.plate}"


class VehicleOwnership(models.Model):
    customer = models.ForeignKey(
        CustomerMembership,
        null=True,
        related_name="ownership",
        on_delete=models.PROTECT,
    )
    owner = models.ForeignKey(
        Owner, null=True, related_name="ownership", on_delete=models.PROTECT
    )
    vehicle = models.OneToOneField(
        Vehicle,
        related_name="ownership",
        verbose_name=_("vehicle"),
        on_delete=models.PROTECT,
    )

    @property
    def pick(self):
        return self.customer or self.owner

    def save(self, *args, **kwargs):
        if self.customer and self.owner:
            raise ValueError(
                "El dueño del vehículo no puede ser cliente y propietario al"
                " mismo tiempo."
            )
        super().save(*args, **kwargs)

    def __str__(self):
        if self.owner:
            return f"{self.owner}"
        elif self.customer:
            return "El cliente es propietario del vehículo."


class QuotationInsuranceVehicle(models.Model):
    insured_amount = models.PositiveIntegerField(_("insured amount"))
    vehicle = models.ForeignKey(
        Vehicle,
        related_name="quotation_insurance_vehicles",
        verbose_name=_("vehicle"),
        on_delete=models.PROTECT,
    )
    consultant_registrar = models.ForeignKey(
        Consultant,
        related_name="quotation_insurance_vehicles_registered",
        verbose_name=_("registrar"),
        on_delete=models.PROTECT,
    )
    consultant_seller = models.ForeignKey(
        Consultant,
        related_name="quotation_insurance_vehicles_sold",
        verbose_name=_("seller"),
        on_delete=models.PROTECT,
    )
    customer = models.ForeignKey(
        CustomerMembership,
        related_name="quotation_insurance_vehicles",
        verbose_name=_("customer"),
        on_delete=models.PROTECT,
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("vehicle insurance quotation")
        verbose_name_plural = _("vehicle insurance quotations")

    @property
    def expired(self):
        return timezone.now() - self.created > timezone.timedelta(days=15)

    def __str__(self):
        return f"insured_amount={self.insured_amount}, vehicle={self.vehicle}"


class InsuranceVehicle(models.Model):
    name = models.CharField(_("name"), max_length=64, unique=True)
    logo = models.ImageField(
        _("logo"), upload_to="insurance_vehicle_images/", blank=True, null=True
    )

    def __str__(self):
        return self.name

    @property
    def last_ratio(self):
        return self.ratios.order_by("-created").first()

    class Meta:
        verbose_name = _("vehicle insurance")
        verbose_name_plural = _("vehicle insurance")


# relación precio - aseguradora
class InsuranceVehicleRatio(models.Model):
    tax = models.DecimalField(
        _("tax (igv)"), decimal_places=2, max_digits=10, null=False
    )
    emission_right = models.DecimalField(
        _("emission right"), decimal_places=2, max_digits=10, null=False
    )
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
    amount = models.DecimalField(
        _("net premium"), decimal_places=2, max_digits=10, default=0
    )
    rate = models.DecimalField(_("rate"), decimal_places=2, max_digits=10)
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
    created = models.DateTimeField(
        _("created at"), auto_now_add=True, unique=True
    )

    @property
    def emission_right(self):
        return round(
            self.amount * self.insurance_vehicle_ratio.emission_right, 2
        )

    @property
    def tax(self):
        value = self.amount + self.emission_right
        return round(value * self.insurance_vehicle_ratio.tax, 2)

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


class IssuanceInsuranceStatus(models.Model):
    name = models.CharField(_("name"), max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("issuance insurance status")
        verbose_name_plural = _("issuance insurance status")


# Issuance
class IssuanceInsuranceVehicle(models.Model):
    # numero de póliza
    number_registry = models.CharField(_("number registry"), max_length=64)

    # fecha de emisión de la póliza
    issuance_date = models.DateTimeField(_("issuance_date"))
    # fecha de vigencia inicio
    initial_validity = models.DateTimeField(_("initial_validity"))
    # fecha de vigencia final
    final_validity = models.DateTimeField(_("final_validity"))

    comment = models.TextField(_("comment"), null=True)

    consultant_registrar = models.ForeignKey(
        Consultant,
        related_name="issuance_insurance_vehicles_registered",
        verbose_name=_("registrar"),
        on_delete=models.PROTECT,
    )
    consultant_seller = models.ForeignKey(
        Consultant,
        related_name="issuance_insurance_vehicles_sold",
        verbose_name=_("seller"),
        on_delete=models.PROTECT,
    )
    consultant_new_sale_rate = models.DecimalField(
        _("consultant new sale rate"), decimal_places=2, max_digits=10
    )
    # estado
    status = models.ForeignKey(
        IssuanceInsuranceStatus,
        related_name="issuances",
        on_delete=models.PROTECT,
    )

    quotation_vehicle_premium = models.ForeignKey(
        QuotationInsuranceVehiclePremium,
        related_name="issuance",
        on_delete=models.PROTECT,
    )

    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.status = IssuanceInsuranceStatus.objects.get(name="Vigente")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("issuance insurance vehicle")
        verbose_name_plural = _("issues insurance vehicle")


class IssuanceInsuranceVehiclePolicy(IssuanceInsuranceVehicle):
    description = models.CharField(_("description"), max_length=64, null=True)


class IssuanceInsuranceVehicleEndorsement(IssuanceInsuranceVehicle):
    commission = models.PositiveIntegerField(_("commission"), null=True)


class IssuanceInsuranceVehicleDocument(models.Model):
    issuance = models.ForeignKey(
        IssuanceInsuranceVehicle,
        related_name="documents",
        on_delete=models.CASCADE,
    )
    file = models.FileField(upload_to="documents/")
    created = models.DateTimeField(auto_now_add=True)


class CollectionInsuranceVehicle(models.Model):
    # fecha de vencimiento
    expiration_date = models.DateTimeField()
    # fecha de pago
    payment_date = models.DateTimeField(null=True)
    # número de factura o boleta
    payment_receipt = models.CharField(max_length=64, null=True)
    # asunto del pago
    issue = models.CharField(max_length=64)
    # monto
    amount = models.DecimalField(decimal_places=2, max_digits=10, null=True)

    issuance_vehicle = models.ForeignKey(
        IssuanceInsuranceVehicle,
        related_name="collections",
        on_delete=models.PROTECT,
    )
    created = models.DateTimeField(auto_now_add=True)

    @property
    def status(self):
        if self.payment_date:
            return "pagado"
        elif (
            self.payment_date is None and self.expiration_date < timezone.now()
        ):
            return "vencido"
        elif (
            self.payment_date is None
            and self.expiration_date - timezone.now()
            <= timezone.timedelta(days=7)
        ):
            return "por vencer"
        elif (
            self.payment_date is None
            and self.expiration_date - timezone.now()
            > timezone.timedelta(days=7)
        ):
            return "pendiente"
        else:
            return "desconocido"

    def __str__(self):
        return f"status={self.status()}"
