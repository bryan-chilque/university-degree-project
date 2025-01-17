from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from rrggweb.utils import to_decimal

from . import validators


class Role(models.Model):
    name = models.CharField(_("name"), max_length=64, unique=True)

    class Meta:
        verbose_name = _("role")
        verbose_name_plural = _("roles")

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(_("name"), max_length=64, unique=True)

    class Meta:
        verbose_name = _("area")
        verbose_name_plural = _("areas")

    def __str__(self):
        return self.name


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
        Area, related_name="consultant", verbose_name=_("area")
    )

    class Meta:
        verbose_name = _("consultant")
        verbose_name_plural = _("consultants")

    def __str__(self):
        return f"{self.given_name} {self.first_surname}"


class ConsultantRate(models.Model):
    new_sale = models.DecimalField(
        _("new sale"), decimal_places=4, max_digits=10
    )
    renewal = models.DecimalField(
        _("renewal"), decimal_places=4, max_digits=10
    )
    consultant = models.OneToOneField(
        Consultant,
        related_name="commission_rate",
        verbose_name=_("consultant"),
        on_delete=models.PROTECT,
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"venta nueva={self.new_sale}, renovación= {self.renewal}"


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
        return f"asesor={self.consultant}, usuario={self.user}"


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
    phone_number = models.CharField(
        _("phone number"),
        max_length=32,
        validators=[validators.only_int],
        null=True,
    )
    email = models.EmailField(_("email"), max_length=64, null=True)
    email2 = models.EmailField(_("email 2"), max_length=64, null=True)
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.PROTECT,
        verbose_name=_("document type"),
    )
    document_number = models.CharField(
        _("document number"),
        max_length=32,
        unique=True,
        validators=[validators.only_int],
    )
    address = models.CharField(_("address"), max_length=128, null=True)

    def clean(self):
        validators.validate_document_number(
            self.document_type, self.document_number
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
        return f"{self.given_name} {self.first_surname} {self.second_surname}"


class LegalPerson(Person):
    # razón social
    registered_name = models.CharField(_("registered name"), max_length=128)
    general_manager = models.CharField(
        _("general manager"), max_length=64, null=True
    )
    anniversary_date = models.DateField(_("anniversary date"), null=True)

    def __str__(self):
        return self.registered_name


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
    seller = models.ForeignKey(
        Consultant,
        on_delete=models.PROTECT,
        related_name="customers",
        verbose_name=_("seller"),
        default=9,
    )

    @property
    def pick(self):
        return self.natural_person or self.legal_person

    def save(self, *args, **kwargs):
        if self.natural_person and self.legal_person:
            raise ValueError(
                "El contratante no puede ser persona natural y jurídica al"
                " mismo tiempo."
            )
        super().save(*args, **kwargs)

    @property
    def type_customer(self):
        if self.natural_person:
            return "Persona natural"
        elif self.legal_person:
            return "Persona jurídica"

    def __str__(self):
        if self.natural_person:
            return f"{self.natural_person}"
        elif self.legal_person:
            return f"{self.legal_person}"


class UseType(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Bank(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    brand = models.CharField(_("brand"), max_length=64)
    vehicle_model = models.CharField(_("model"), max_length=64)
    plate = models.CharField(_("plate"), max_length=64, unique=True, null=True)
    fabrication_year = models.PositiveIntegerField(_("fabrication year"))
    engine = models.CharField(_("engine number"), max_length=64)
    chassis = models.CharField(_("chassis number"), max_length=64)
    seat_number = models.PositiveIntegerField(_("seat number"))
    # vehículo gps
    has_gps = models.BooleanField(_("has gps?"), default=False)
    # vehículo tiene endoso
    has_endorsee = models.BooleanField(_("has endorsee?"), default=False)
    endorsement_bank = models.ForeignKey(
        Bank,
        verbose_name=_("endorsement bank"),
        on_delete=models.PROTECT,
        null=True,
    )
    use_type = models.ForeignKey(
        UseType,
        related_name="use_type",
        verbose_name=_("usage"),
        on_delete=models.PROTECT,
    )
    class_type = models.CharField(_("class"), max_length=64, null=True)

    def save(self, *args, **kwargs):
        if not self.has_endorsee:
            self.endorsee_bank = None
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("vehicle")
        verbose_name_plural = _("vehicles")

    def __str__(self):
        return f"{self.plate}"


class VehicleOwnership(models.Model):
    customer = models.ForeignKey(
        CustomerMembership,
        null=True,
        related_name="ownership",
        on_delete=models.PROTECT,
    )
    owner = models.ForeignKey(
        NaturalPerson,
        null=True,
        related_name="ownership",
        on_delete=models.PROTECT,
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
                f"El vehículo con placa {self.vehicle.plate} no puede tener 2"
                " propietarios."
            )
        super().save(*args, **kwargs)

    def __str__(self):
        if self.owner:
            return f"{self.owner}"
        elif self.customer:
            return "El contratante es el asegurado."


class InsuranceVehicle(models.Model):
    name = models.CharField(_("name"), max_length=64, unique=True)
    logo = models.ImageField(
        _("logo"), upload_to="insurance_vehicle_images/", blank=True, null=True
    )

    @property
    def last_ratio(self):
        return self.ratios.order_by("-created").first()

    class Meta:
        verbose_name = _("vehicle insurance")
        verbose_name_plural = _("vehicle insurance")

    def __str__(self):
        return self.name


# relación precio - aseguradoras
class InsuranceVehicleRatio(models.Model):
    tax = models.DecimalField(_("tax (igv)"), decimal_places=4, max_digits=10)
    emission_right = models.DecimalField(
        _("emission right"), decimal_places=4, max_digits=10
    )
    created = models.DateTimeField(auto_now_add=True)
    insurance_vehicle = models.ForeignKey(
        InsuranceVehicle, related_name="ratios", on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = _("vehicle insurance ratio")
        verbose_name_plural = _("vehicle insurance ratios")

    def __str__(self):
        return f"{self.insurance_vehicle}"


class Risk(models.Model):
    name = models.CharField(_("name"), max_length=64, unique=True)

    class Meta:
        verbose_name = _("risk")
        verbose_name_plural = _("risks")

    def __str__(self):
        return self.name


class RiskInsuranceVehicle(models.Model):
    risk = models.ForeignKey(Risk, on_delete=models.PROTECT)
    insurance_vehicle = models.ForeignKey(
        InsuranceVehicle, on_delete=models.PROTECT
    )

    def __str__(self):
        return f"riesgo={self.risk}, Cia={self.insurance_vehicle}"


class InsurancePlan(models.Model):
    name = models.CharField(_("name"), max_length=64)
    commission = models.DecimalField(
        _("commission"), decimal_places=4, max_digits=10
    )
    risk_insurance_vehicle = models.ForeignKey(
        RiskInsuranceVehicle,
        related_name="plans",
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = _("insurance plan")
        verbose_name_plural = _("insurance plans")

    def __str__(self):
        return self.name


class QuotationInsurance(models.Model):
    risk = models.ForeignKey(
        Risk,
        related_name="quotation_insurances",
        verbose_name=_("risk"),
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
        null=True,
    )
    customer = models.ForeignKey(
        CustomerMembership,
        related_name="quotation_insurance_vehicles",
        verbose_name=_("customer"),
        on_delete=models.PROTECT,
    )
    # moneda
    currency = models.ForeignKey(
        Currency,
        related_name="quotation_insurance_vehicles",
        verbose_name=_("currency"),
        on_delete=models.PROTECT,
    )
    source = models.CharField(_("source"), max_length=64)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        verbose_name = _("insurance quotation")
        verbose_name_plural = _("insurance quotations")


class QuotationInsuranceVehicle(QuotationInsurance):
    insured_amount = models.DecimalField(
        _("insured amount"), decimal_places=2, max_digits=10
    )
    vehicle = models.ForeignKey(
        Vehicle,
        related_name="quotation_insurance_vehicles",
        verbose_name=_("vehicle"),
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = _("vehicle insurance quotation")
        verbose_name_plural = _("vehicle insurance quotations")

    @property
    def expired(self):
        return timezone.now() - self.created > timezone.timedelta(days=15)

    def __str__(self):
        return f"suma asegurada={self.insured_amount}, vehículo={self.vehicle}"


class QuotationInsuranceVehiclePremium(models.Model):
    # prima neta
    amount = models.DecimalField(
        _("net premium"), decimal_places=2, max_digits=10, default=0
    )
    rate = models.DecimalField(_("rate"), decimal_places=4, max_digits=10)
    tax_percentage = models.DecimalField(
        _("tax percentage"), decimal_places=4, max_digits=10, default=0.18
    )
    emission_right_percentage = models.DecimalField(
        _("emission right percentage"),
        decimal_places=4,
        max_digits=10,
        default=0.03,
    )
    insurance_vehicle_ratio = models.ForeignKey(
        InsuranceVehicleRatio,
        related_name="quotation_insurance_vehicle_premiums",
        verbose_name=_("vehicle insurance ratio"),
        on_delete=models.PROTECT,
    )
    quotation_insurance_vehicle = models.ForeignKey(
        QuotationInsuranceVehicle,
        related_name="premiums",
        on_delete=models.PROTECT,
    )
    # para venta múltiple
    in_progress = models.BooleanField(_("in progress"), default=False)
    # para renovación múltiple
    renewal_in_progress = models.BooleanField(
        _("renewal in progress"), default=False
    )
    created = models.DateTimeField(_("created at"), auto_now_add=True)

    @property
    def emission_right(self):
        amount = self.amount * self.emission_right_percentage
        return to_decimal(amount)

    # prima comercial
    @property
    def commercial_premium(self):
        amount = self.amount + self.emission_right
        return to_decimal(amount)

    @property
    def tax(self):
        amount = self.commercial_premium * self.tax_percentage
        return to_decimal(amount)

    # prima total
    @property
    def total(self):
        amount = self.commercial_premium + self.tax
        return to_decimal(amount)

    # fee
    @property
    def fee(self):
        return round(self.total / 4, 2)

    # direct_debit
    @property
    def direct_debit(self):
        return round(self.total / 12, 2)

    def __str__(self):
        return f"prima neta={self.amount}, total={self.total}"


class IssuanceInsuranceStatus(models.Model):
    name = models.CharField(_("name"), max_length=64, unique=True)

    class Meta:
        verbose_name = _("issuance insurance status")
        verbose_name_plural = _("issuance insurance status")

    def __str__(self):
        return self.name


class IssuanceInsuranceType(models.Model):
    name = models.CharField(_("name"), max_length=64, unique=True)

    class Meta:
        verbose_name = _("issuance insurance type")
        verbose_name_plural = _("issuance insurance type")

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    name = models.CharField(_("name"), max_length=64, unique=True)

    class Meta:
        verbose_name = _("payment method")
        verbose_name_plural = _("payment methods")

    def __str__(self):
        return self.name


# emisión de seguro / póliza
class IssuanceInsurance(models.Model):
    # numero de póliza
    policy = models.CharField(_("policy number"), max_length=64)
    # documento de cobranza
    collection_document = models.CharField(
        _("collection document"), max_length=64
    )
    # fecha de emisión de la póliza
    issuance_date = models.DateField(_("issuance date"))
    # fecha de vigencia inicio
    initial_validity = models.DateField(_("initial validity"))
    # fecha de vigencia final
    final_validity = models.DateField(_("final validity"))
    # kcs_commission
    plan_commission_percentage = models.DecimalField(
        _("plan commission percentage"),
        decimal_places=4,
        max_digits=10,
    )
    comment = models.TextField(_("comment"), null=True)

    issuance_type = models.ForeignKey(
        IssuanceInsuranceType,
        related_name="issuances",
        on_delete=models.PROTECT,
        default=1,
    )
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
    seller_commission_percentage = models.DecimalField(
        _("seller commission percentage"),
        decimal_places=4,
        max_digits=10,
    )
    # estado
    status = models.ForeignKey(
        IssuanceInsuranceStatus,
        related_name="issuances",
        on_delete=models.PROTECT,
    )
    insurance_plan = models.ForeignKey(
        InsurancePlan,
        related_name="issuances",
        on_delete=models.PROTECT,
    )
    # forma de pago
    payment_method = models.ForeignKey(
        PaymentMethod,
        related_name="issuances",
        verbose_name=_("payment method"),
        on_delete=models.PROTECT,
    )
    # fecha de registro
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.status_id = 1
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        verbose_name = _("issuance insurance vehicle")
        verbose_name_plural = _("issues insurance vehicle")


class IssuanceInsuranceVehicle(IssuanceInsurance):
    quotation_vehicle_premiums = models.ManyToManyField(
        QuotationInsuranceVehiclePremium,
        related_name="issuances",
    )

    @property
    def insured_amount(self):
        premiums = self.quotation_vehicle_premiums.all()
        quotations = []
        for premium in premiums:
            quotations.append(premium.quotation_insurance_vehicle)
        amount = sum(quotation.insured_amount for quotation in quotations)
        return to_decimal(amount)

    @property
    def net_premium(self):
        premiums = self.quotation_vehicle_premiums.all()
        amount = sum(premium.amount for premium in premiums)
        return to_decimal(amount)

    @property
    def rate(self):
        return self.net_premium / self.insured_amount

    @property
    def emission_right(self):
        premium = self.quotation_vehicle_premiums.first()
        amount = self.net_premium * premium.emission_right_percentage
        return to_decimal(amount)

    @property
    def commercial_premium(self):
        amount = self.net_premium + self.emission_right
        return to_decimal(amount)

    @property
    def tax(self):
        premium = self.quotation_vehicle_premiums.first()
        amount = self.commercial_premium * premium.tax_percentage
        return to_decimal(amount)

    @property
    def total_premium(self):
        return self.commercial_premium + self.tax

    @property
    def net_commission(self):
        premiums = self.quotation_vehicle_premiums.all()
        amount = (
            sum(premium.amount for premium in premiums)
            * self.plan_commission_percentage
        )  # noqa
        return to_decimal(amount)

    @property
    def seller_commission(self):
        amount = self.seller_commission_percentage * self.net_commission
        return to_decimal(amount)

    @property
    def kcs_commission(self):
        amount = self.net_commission - self.seller_commission
        return to_decimal(amount)


class IssuanceInsuranceVehicleDocument(models.Model):
    issuance = models.ForeignKey(
        IssuanceInsuranceVehicle,
        related_name="documents",
        on_delete=models.CASCADE,
    )
    file = models.FileField(upload_to="documents/")
    created = models.DateTimeField(auto_now_add=True)


class Endorsement(models.Model):
    insured_amount = models.DecimalField(
        _("insured amount"), decimal_places=2, max_digits=10
    )
    net_premium = models.DecimalField(
        _("net premium"), decimal_places=2, max_digits=10, default=0
    )
    rate = models.DecimalField(_("rate"), decimal_places=4, max_digits=10)
    tax_percentage = models.DecimalField(
        _("tax percentage"), decimal_places=4, max_digits=10, default=0.18
    )
    emission_right_percentage = models.DecimalField(
        _("emission right percentage"),
        decimal_places=4,
        max_digits=10,
        default=0.03,
    )
    # documento de cobranza
    collection_document = models.CharField(
        _("collection document"), max_length=64
    )
    # fecha de emisión de la póliza
    issuance_date = models.DateField(_("issuance date"))
    # fecha de vigencia inicio
    initial_validity = models.DateField(_("initial validity"))
    # fecha de vigencia final
    final_validity = models.DateField(_("final validity"))
    # porcentaje de comisión del plan de seguro
    plan_commission_percentage = models.DecimalField(
        _("plan commission percentage"),
        decimal_places=4,
        max_digits=10,
    )
    seller_commission_percentage = models.DecimalField(
        _("seller commission percentage"),
        decimal_places=4,
        max_digits=10,
    )
    detail = models.TextField(_("detail"))
    currency = models.ForeignKey(
        Currency,
        related_name="endorsements",
        verbose_name=_("currency"),
        on_delete=models.PROTECT,
    )
    # forma de pago
    payment_method = models.ForeignKey(
        PaymentMethod,
        related_name="endorsements",
        verbose_name=_("payment method"),
        on_delete=models.PROTECT,
    )

    @property
    def emission_right(self):
        amount = self.net_premium * self.emission_right_percentage
        return to_decimal(amount)

    @property
    def commercial_premium(self):
        amount = self.net_premium + self.emission_right
        return to_decimal(amount)

    @property
    def tax(self):
        amount = self.commercial_premium * self.tax_percentage
        return to_decimal(amount)

    @property
    def total(self):
        amount = self.commercial_premium + self.tax
        return to_decimal(amount)

    @property
    def net_commission(self):
        amount = self.net_premium * self.plan_commission_percentage
        return to_decimal(amount)

    @property
    def seller_commission(self):
        amount = self.seller_commission_percentage * self.net_commission
        return to_decimal(amount)

    @property
    def kcs_commission(self):
        amount = self.net_commission - self.seller_commission
        return to_decimal(amount)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        verbose_name = _("endorsement")
        verbose_name_plural = _("endorsements")


class EndorsementVehicle(Endorsement):
    vehicle = models.ForeignKey(
        Vehicle,
        related_name="endorsements",
        on_delete=models.CASCADE,
    )


class CollectionInsuranceVehicle(models.Model):
    # fecha de vencimiento
    expiration_date = models.DateField()
    # fecha de pago
    payment_date = models.DateField(null=True)
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


# Modelo para la data histórica


class HistoricalData(models.Model):
    register_date = models.CharField(max_length=128, null=True)
    collection_record_date = models.CharField(max_length=128, null=True)
    customer = models.CharField(max_length=128, null=True)
    document_number = models.CharField(max_length=32, null=True)
    birth_date = models.CharField(max_length=128, null=True)
    consultant = models.CharField(max_length=128, null=True)
    consultant_type = models.CharField(max_length=128, null=True)
    risk = models.CharField(max_length=128, null=True)
    policy = models.CharField(max_length=128, null=True)
    insurance_plan = models.CharField(max_length=128, null=True)
    insurance_vehicle = models.CharField(max_length=128, null=True)
    issuance_date = models.CharField(max_length=128, null=True)
    payment_document = models.CharField(max_length=128, null=True)
    expiration_date_first_coupon = models.CharField(max_length=128, null=True)
    initial_validity = models.CharField(max_length=128, null=True)
    final_validity = models.CharField(max_length=128, null=True)
    payment_date = models.CharField(max_length=128, null=True)
    payment_status_first_coupon = models.CharField(max_length=128, null=True)
    currency = models.CharField(max_length=128, null=True)
    status = models.CharField(max_length=128, null=True)
    observations = models.CharField(max_length=128, null=True)
    insured_amount = models.CharField(max_length=128, null=True)
    kcs_commission_percentage = models.CharField(max_length=128, null=True)
    net_premium = models.CharField(max_length=128, null=True)
    commercial_premium = models.CharField(max_length=128, null=True)
    total_premium = models.CharField(max_length=128, null=True)
    net_commission_amount = models.CharField(max_length=128, null=True)
    payment_method = models.CharField(max_length=128, null=True)
    months = models.CharField(max_length=128, null=True)
    year = models.CharField(max_length=128, null=True)
    dolar_premium = models.CharField(max_length=128, null=True)
    dolar_commission = models.CharField(max_length=128, null=True)
    email = models.CharField(max_length=128, null=True)
    policy_address = models.CharField(max_length=128, null=True)
    phone_number = models.CharField(max_length=128, null=True)
    phone_number2 = models.CharField(max_length=128, null=True)
