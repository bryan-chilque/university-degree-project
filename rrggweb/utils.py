from decimal import ROUND_HALF_UP, Decimal
from typing import NamedTuple


class SeguroItem(NamedTuple):
    name: str
    url: str


def to_decimal(amount):
    str_amount = str(amount)
    dot_index = str_amount.find(".")
    if dot_index != -1:
        # truncamiento a 2 dígitos
        # str_amount = str_amount[: dot_index + 3]
        # redondeo a 2 dígitos
        str_amount = Decimal(str_amount).quantize(
            Decimal("0.00"), rounding=ROUND_HALF_UP
        )
    return Decimal(str_amount)
