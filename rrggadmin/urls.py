from django.urls import include, path

from . import views

insurance_vehicle_price_urlpatterns = (
    [
        path(
            "list/", views.InsuranceVehiclePriceListView.as_view(), name="list"
        ),
        path(
            "create/",
            views.InsuranceVehiclePriceCreateView.as_view(),
            name="create",
        ),
    ],
    "price",
)

insurance_vehicle_urlpatterns = (
    [
        path("list/", views.InsuraceVehicleListView.as_view(), name="list"),
        path(
            "create/", views.InsuraceVehicleCreateView.as_view(), name="create"
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

consultant_urlpatterns = (
    [
        path("list/", views.ConsultantListView.as_view(), name="list"),
        path("create/", views.ConsultantCreateView.as_view(), name="create"),
    ],
    "consultant",
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

app_name = "rrggadmin"


urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("home/", views.HomeView.as_view(), name="home"),
    path("insurance/", include(insurance_urlpatterns)),
    path("consultant/", include(consultant_urlpatterns)),
    path("user/", include(user_urlpatterns)),
    path("consultant_membership/", include(consultant_membership_urlpatterns)),
]
