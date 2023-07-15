from django import urls
from django.contrib.auth import views as views_auth
from django.views.generic import TemplateView, CreateView

import rrgg.models

from .utils import SeguroItem


class LoginView(views_auth.LoginView):
    template_name = "rrggweb/login.html"
    next_page = urls.reverse_lazy("rrggweb:home")

# HOME
class HomeView(TemplateView):
    template_name = "rrggweb/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seguros"] = [
            SeguroItem(
                "Seguro de vehicular", urls.reverse("rrggweb:quotation:insurance:vehicle:list")
            ),
            SeguroItem("Seguro de vida", ""),
            SeguroItem("Seguro de accidentes", ""),
            SeguroItem("Seguro de salud", ""),
        ]
        return context

# QUOTATION INSURANCE VEHICLE
class QuotationInsuranceVehicleListView(TemplateView):
    template_name = "rrggweb/quotation/insurance/vehicle/list.html"

class QuotationInsuranceVehicleCreateView(CreateView):
    template_name = "rrggweb/quotation/insurance/vehicle/create.html"
    success_url = urls.reverse_lazy("rrggweb:quotation_insurance_vehicle")
    model = rrgg.models.QuotationInsuranceVehicle
    fields = "__all__"
