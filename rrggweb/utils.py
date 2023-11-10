from decimal import Decimal
from typing import NamedTuple


class SeguroItem(NamedTuple):
    name: str
    url: str


def to_decimal(amount):
    str_amount = str(amount)
    dot_index = str_amount.find(".")
    if dot_index != -1:
        str_amount = str_amount[: dot_index + 3]
    return Decimal(str_amount)
