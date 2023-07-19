from nomos.views.generic.list import MultipleObjectMixin


class ListMixin(MultipleObjectMixin):
    paginate_by = 10
