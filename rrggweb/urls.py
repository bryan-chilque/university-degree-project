from django.urls import include, path

from . import views

app_name = "rrggweb"

quotation_insurance_vehicle_urlpatterns = (
    [
        path(
            "list/",
            views.QuotationInsuranceVehicleListView.as_view(),
            name="list",
        ),
        path(
            "create/",
            views.QuotationInsuranceVehicleCreateView.as_view(),
            name="create",
        ),
    ],
    "vehicle",
)

quotation_insurance_urlpatterns = (
    [path("vehicle/", include(quotation_insurance_vehicle_urlpatterns))],
    "insurance",
)

quotation_urlpatterns = (
    [path("insurance/", include(quotation_insurance_urlpatterns))],
    "quotation",
)

urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("quotation/", include(quotation_urlpatterns)),
]
