from django.urls import include, path
from nomos.urls import menu_patterns
from nomos.views.generic.detail import PairFieldsMixin
from nomos.views.generic.menu import MenuTraits, ViewTraits

import rrgg.models

from . import mixins, views

insurance_vehicle_menu_patterns = menu_patterns(
    rrgg.models.InsuranceVehicle,
    "rrggadmin/insurance/vehicle",
    "vehicle",
    "rrggadmin:insurance",
    menu_traits=MenuTraits(
        list=ViewTraits(bases=[mixins.ListMixin]),
        detail=ViewTraits(bases=[PairFieldsMixin]),
    ),
)

insurance_vehicle_price_urlpatterns2 = menu_patterns(
    rrgg.models.InsuranceVehicleRatio,
    "rrggadmin/common",
    "ratios",
    "rrggadmin:insurance_vehicle",
    menu_traits=MenuTraits(
        list=ViewTraits(bases=[mixins.ListMixin]),
        detail=ViewTraits(bases=[PairFieldsMixin]),
    ),
)

insurance_vehicle_ratios_urlpatterns = (
    [path("ratios/", include(insurance_vehicle_price_urlpatterns2))],
    "insurance_vehicle",
)

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
        path(
            "<int:pk>/update/",
            views.InsuranceVehicleRatioUpdateView.as_view(),
            name="update",
        ),
        path(
            "<int:pk>/detail/",
            views.InsuranceVehicleRatioDetailView.as_view(),
            name="detail",
        ),
    ],
    "price",
)

insurance_vehicle_menu_patterns = (
    [
        *insurance_vehicle_menu_patterns[0],
        path(
            "<int:insurance_vehicle_id>/price/",
            include(insurance_vehicle_price_urlpatterns),
        ),
    ],
    insurance_vehicle_menu_patterns[1],
)

insurance_urlpatterns = (
    [
        path("vehicle/", include(insurance_vehicle_menu_patterns)),
    ],
    "insurance",
)


# MENU PATTERNS


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

role_urlpatterns = menu_patterns(
    rrgg.models.Role,
    "rrggadmin/common",
    "role",
    "rrggadmin",
    menu_traits=MenuTraits(
        list=ViewTraits(bases=[mixins.ListMixin]),
        detail=ViewTraits(bases=[PairFieldsMixin]),
    ),
)

area_urlpatterns = menu_patterns(
    rrgg.models.Area,
    "rrggadmin/common",
    "area",
    "rrggadmin",
    menu_traits=MenuTraits(
        list=ViewTraits(bases=[mixins.ListMixin]),
        detail=ViewTraits(bases=[PairFieldsMixin]),
    ),
)

consultant_rate_urlpatterns = menu_patterns(
    rrgg.models.ConsultantRate,
    "rrggadmin/common",
    "consultant_rate",
    "rrggadmin",
    menu_traits=MenuTraits(
        list=ViewTraits(bases=[mixins.ListMixin]),
        detail=ViewTraits(bases=[PairFieldsMixin]),
    ),
)

risk_urlpatterns = menu_patterns(
    rrgg.models.Risk,
    "rrggadmin/common",
    "risk",
    "rrggadmin",
    menu_traits=MenuTraits(
        list=ViewTraits(bases=[mixins.ListMixin]),
        detail=ViewTraits(bases=[PairFieldsMixin]),
    ),
)

risk_insurance_vehicle_urlpatterns = menu_patterns(
    rrgg.models.RiskInsuranceVehicle,
    "rrggadmin/common",
    "risk_insurance_vehicle",
    "rrggadmin",
    menu_traits=MenuTraits(
        list=ViewTraits(bases=[mixins.ListMixin]),
        detail=ViewTraits(bases=[PairFieldsMixin]),
    ),
)

insurance_plan_urlpatterns = menu_patterns(
    rrgg.models.InsurancePlan,
    "rrggadmin/common",
    "insurance_plan",
    "rrggadmin",
    menu_traits=MenuTraits(
        list=ViewTraits(bases=[mixins.ListMixin]),
        detail=ViewTraits(bases=[PairFieldsMixin]),
    ),
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

issuanceInsuranceStatus_urlpatterns = menu_patterns(
    rrgg.models.IssuanceInsuranceStatus,
    "rrggadmin/common",
    "issuance_insurance_status",
    "rrggadmin",
    menu_traits=MenuTraits(
        list=ViewTraits(bases=[mixins.ListMixin]),
        detail=ViewTraits(bases=[PairFieldsMixin]),
    ),
)

issuanceInsuranceType_urlpatterns = menu_patterns(
    rrgg.models.IssuanceInsuranceType,
    "rrggadmin/common",
    "issuance_insurance_type",
    "rrggadmin",
    menu_traits=MenuTraits(
        list=ViewTraits(bases=[mixins.ListMixin]),
        detail=ViewTraits(bases=[PairFieldsMixin]),
    ),
)

bank_urlpatterns = menu_patterns(
    rrgg.models.Bank,
    "rrggadmin/common",
    "bank",
    "rrggadmin",
    menu_traits=MenuTraits(
        list=ViewTraits(bases=[mixins.ListMixin]),
        detail=ViewTraits(bases=[PairFieldsMixin]),
    ),
)

currency_urlpatterns = menu_patterns(
    rrgg.models.Currency,
    "rrggadmin/common",
    "currency",
    "rrggadmin",
    menu_traits=MenuTraits(
        list=ViewTraits(bases=[mixins.ListMixin]),
        detail=ViewTraits(bases=[PairFieldsMixin]),
    ),
)

payment_method_urlpatterns = menu_patterns(
    rrgg.models.PaymentMethod,
    "rrggadmin/common",
    "payment_method",
    "rrggadmin",
    menu_traits=MenuTraits(
        list=ViewTraits(bases=[mixins.ListMixin]),
        detail=ViewTraits(bases=[PairFieldsMixin]),
    ),
)

document_type_urlpatterns = menu_patterns(
    rrgg.models.DocumentType,
    "rrggadmin/common",
    "document_type",
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
    path("role/", include(role_urlpatterns)),
    path("area/", include(area_urlpatterns)),
    path("insurance/", include(insurance_urlpatterns)),
    path("consultant/", include(consultant_urlpatterns)),
    path("use_type/", include(use_type_urlpatterns)),
    path("user/", include(user_urlpatterns)),
    path("consultant_membership/", include(consultant_membership_urlpatterns)),
    path("consultant_rate/", include(consultant_rate_urlpatterns)),
    path("risk/", include(risk_urlpatterns)),
    path("insurance_vehicle/", include(insurance_vehicle_ratios_urlpatterns)),
    path(
        "risk_insurance_vehicle/", include(risk_insurance_vehicle_urlpatterns)
    ),
    path("insurance_plan/", include(insurance_plan_urlpatterns)),
    path(
        "issuance_insurance_status/",
        include(issuanceInsuranceStatus_urlpatterns),
    ),
    path(
        "issuance_insurance_type/",
        include(issuanceInsuranceType_urlpatterns),
    ),
    path("bank/", include(bank_urlpatterns)),
    path("currency/", include(currency_urlpatterns)),
    path("payment_method/", include(payment_method_urlpatterns)),
    path("document_type/", include(document_type_urlpatterns)),
]
