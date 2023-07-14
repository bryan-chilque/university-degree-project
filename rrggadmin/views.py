from django import urls
from django.contrib.auth import views as views_auth
from django.views.generic import CreateView, ListView, TemplateView

import rrgg.models


class LoginView(views_auth.LoginView):
    template_name = "rrggadmin/login.html"
    next_page = urls.reverse_lazy("rrggadmin:home")


class HomeView(TemplateView):
    template_name = "rrggadmin/home.html"


class SeguroVehicularCreateView(CreateView):
    template_name = "rrggadmin/seguro/vehicular/create.html"
    success_url = urls.reverse_lazy("rrggadmin:seguro:vehicular:list")
    model = rrgg.models.InsuranceVehiclePrice
    fields = "__all__"


class SeguroVehicularListView(ListView):
    template_name = "rrggadmin/seguro/vehicular/list.html"
    model = rrgg.models.InsuranceVehiclePrice


class ConsultantListView(ListView):
    template_name = "rrggadmin/consultant/list.html"
    model = rrgg.models.Consultant


class ConsultantCreateView(CreateView):
    template_name = "rrggadmin/consultant/create.html"
    success_url = urls.reverse_lazy("rrggadmin:consultant:list")
    model = rrgg.models.Consultant
    fields = "__all__"
