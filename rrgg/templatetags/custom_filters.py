from decimal import ROUND_HALF_UP, Decimal

from django import template

register = template.Library()


@register.filter(name="to_two_decimals")
def to_two_decimals(value):
    value = float(value)
    return "{:.2f}".format(value).replace(".", ",")


@register.filter(name="to_percentage")
def to_percentage(value):
    if value is not None:
        value = Decimal(value * 100).quantize(
            Decimal("0.00"), rounding=ROUND_HALF_UP
        )
        if value % 1 == 0:
            return "{:.0f}%".format(value)
        else:
            return "{:.2f}%".format(value).replace(".", ",")
    else:
        return ""
