from django.urls import include, path

from . import views

quotation_insurance_vehicle_urlpatterns = (
    [
        path(
            "list/",
            views.QuotationInsuranceVehicleListView.as_view(),
            name="list",
        ),
        path(
            "create/customer/<int:customer_id>/vehicle/<int:vehicle_id>/",
            views.QuotationInsuranceVehicleCreateView.as_view(),
            name="create",
        ),
        path(
            "search/",
            views.QuotationInsuranceVehicleSearchView.as_view(),
            name="search",
        ),
        path(
            "create_vehicle/customer/<int:customer_id>/",
            views.QuotationInsuranceVehicleCreateVehicleView.as_view(),
            name="create_vehicle",
        ),
        path(
            "create_customer/",
            views.QuotationInsuranceVehicleCreateCustomerView.as_view(),
            name="create_customer",
        ),
        path(
            "update_customer/<int:customer_id>/",
            views.QuotationInsuranceVehicleUpdateCustomerView.as_view(),
            name="update_customer",
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

app_name = "rrggweb"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("<int:consultant_id>/home/", views.HomeView.as_view(), name="home"),
    path("<int:consultant_id>/quotation/", include(quotation_urlpatterns)),
]
