from django.urls import include, path
from nomos.urls import menu_patterns
from nomos.views.generic.detail import PairFieldsMixin
from nomos.views.generic.menu import MenuTraits, ViewTraits

import rrgg.models

from . import mixins, views

insurance_vehicle_price_urlpatterns = (
    [
        path(
            "list/", views.InsuranceVehicleRatioListView.as_view(), name="list"
        ),
        path(
            "create/",
            views.InsuranceVehicleRatioCreateView.as_view(),
            name="create",
        ),
    ],
    "price",
)

insurance_vehicle_urlpatterns = (
    [
        path("list/", views.InsuranceVehicleListView.as_view(), name="list"),
        path(
            "create/",
            views.InsuranceVehicleCreateView.as_view(),
            name="create",
        ),
        path(
            "<int:insurance_vehicle_id>/price/",
            include(insurance_vehicle_price_urlpatterns),
        ),
    ],
    "vehicle",
)

insurance_urlpatterns = (
    [
        path("vehicle/", include(insurance_vehicle_urlpatterns)),
    ],
    "insurance",
)

consultant_urlpatterns = menu_patterns(
    rrgg.models.Consultant,
    "rrggadmin/common",
    "consultant",
    "rrggadmin",
    menu_traits=MenuTraits(
        list=ViewTraits(bases=[mixins.ListMixin]),
        detail=ViewTraits(bases=[PairFieldsMixin]),
    ),
)


user_urlpatterns = (
    [
        path("list/", views.UserListView.as_view(), name="list"),
        path("create/", views.UserCreateView.as_view(), name="create"),
    ],
    "user",
)

consultant_membership_urlpatterns = (
    [
        path(
            "list/", views.ConsultantMembershipListView.as_view(), name="list"
        ),
        path(
            "create/",
            views.ConsultantMembershipCreateView.as_view(),
            name="create",
        ),
    ],
    "consultant_membership",
)

use_type_urlpatterns = menu_patterns(
    rrgg.models.UseType,
    "rrggadmin/common",
    "use_type",
    "rrggadmin",
    menu_traits=MenuTraits(
        list=ViewTraits(bases=[mixins.ListMixin]),
        detail=ViewTraits(bases=[PairFieldsMixin]),
    ),
)

app_name = "rrggadmin"


urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("home/", views.HomeView.as_view(), name="home"),
    path("insurance/", include(insurance_urlpatterns)),
    path("consultant/", include(consultant_urlpatterns)),
    path("use_type/", include(use_type_urlpatterns)),
    path("user/", include(user_urlpatterns)),
    path("consultant_membership/", include(consultant_membership_urlpatterns)),
]
