from django import shortcuts, urls
from django.contrib.auth import views as views_auth
from django.views.generic import CreateView, ListView, TemplateView

import rrgg.models


class LoginView(views_auth.LoginView):
    template_name = "rrggadmin/login.html"
    next_page = urls.reverse_lazy("rrggadmin:home")


class HomeView(TemplateView):
    template_name = "rrggadmin/home.html"


# USERS
class UserListView(ListView):
    template_name = "rrggadmin/user/list.html"
    model = rrgg.models.get_user_model()


class UserCreateView(CreateView):
    template_name = "rrggadmin/user/create.html"
    success_url = urls.reverse_lazy("rrggadmin:user:list")
    model = rrgg.models.get_user_model()
    fields = ["username", "password"]

    def form_valid(self, form):
        form.instance.set_password(form.instance.password)
        return super().form_valid(form)


# CONSULTANT MEMBERSHIP
class ConsultantMembershipListView(ListView):
    template_name = "rrggadmin/consultant_membership/list.html"
    model = rrgg.models.ConsultantMembership


class ConsultantMembershipCreateView(CreateView):
    template_name = "rrggadmin/consultant_membership/create.html"
    success_url = urls.reverse_lazy("rrggadmin:consultant_membership:list")
    model = rrgg.models.ConsultantMembership
    fields = "__all__"


# INSURANCE VEHICLE


class InsuraceVehicleCreateView(CreateView):
    template_name = "rrggadmin/insurance/vehicle/create.html"
    success_url = urls.reverse_lazy("rrggadmin:insurance:vehicle:list")
    model = rrgg.models.InsuranceVehicle
    fields = "__all__"


class InsuraceVehicleListView(ListView):
    template_name = "rrggadmin/insurance/vehicle/list.html"
    model = rrgg.models.InsuranceVehicle


# INSURANCE VEHICLE PRICE


class InsuranceVehiclePriceListView(ListView):
    template_name = "rrggadmin/insurance/vehicle/price/list.html"
    model = rrgg.models.InsuranceVehiclePrice

    def get_queryset(self):
        return rrgg.models.InsuranceVehiclePrice.objects.filter(
            insurance_vehicle__id=self.kwargs["insurance_vehicle_id"]
        )


class InsuranceVehiclePriceCreateView(CreateView):
    template_name = "rrggadmin/insurance/vehicle/price/create.html"
    model = rrgg.models.InsuranceVehiclePrice
    fields = "business_premium", "emission_right", "tax"

    def get_success_url(self):
        return urls.reverse(
            "rrggadmin:insurance:vehicle:price:list",
            args=[self.kwargs["insurance_vehicle_id"]],
        )

    def form_valid(self, form):
        insurance_vehicle = shortcuts.get_object_or_404(
            rrgg.models.InsuranceVehicle,
            id=self.kwargs["insurance_vehicle_id"],
        )
        form.instance.insurance_vehicle = insurance_vehicle
        return super().form_valid(form)


# CONSULTANT


class ConsultantListView(ListView):
    template_name = "rrggadmin/consultant/list.html"
    model = rrgg.models.Consultant


class ConsultantCreateView(CreateView):
    template_name = "rrggadmin/consultant/create.html"
    success_url = urls.reverse_lazy("rrggadmin:consultant:list")
    model = rrgg.models.Consultant
    fields = "__all__"
