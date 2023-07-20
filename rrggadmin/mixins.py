from typing import Any, Dict
from nomos.views.generic.list import MultipleObjectMixin
from django.views.generic.detail import View

class ListMixin(MultipleObjectMixin):
    paginate_by = 10
    