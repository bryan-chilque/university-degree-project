from django import template

register = template.Library()


@register.filter(name="to_two_decimals")
def to_two_decimals(value):
    value = float(value)
    return "{:.2f}".format(value).replace(".", ",")


@register.filter(name="to_percentage")
def to_percentage(value):
    if value is not None:
        value = float(value) * 100
        if value.is_integer():
            return "{:.0f}%".format(value)
        else:
            return "{:.2f}%".format(value).replace(".", ",")
    else:
        return ""
