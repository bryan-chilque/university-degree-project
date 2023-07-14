from django import urls
from django.contrib.auth import views as views_auth
from django.views.generic.base import TemplateView

from .utils import SeguroItem


class LoginView(views_auth.LoginView):
    template_name = "rrggweb/login.html"
    next_page = urls.reverse_lazy("rrggweb:home")


class HomeView(TemplateView):
    template_name = "rrggweb/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seguros"] = [
            SeguroItem(
                "Seguro de vehicular", urls.reverse("rrggweb:seguro_vehicular")
            ),
            SeguroItem("Seguro de vida", ""),
            SeguroItem("Seguro de accidentes", ""),
            SeguroItem("Seguro de salud", ""),
        ]
        return context


class SeguroVehicularView(TemplateView):
    template_name = "rrggweb/seguro_vehicular.html"
