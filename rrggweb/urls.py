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
            (
                "customer/<int:customer_id>/vehicle/<int:vehicle_id>"
                "/quotation/<int:quotation_id>/create_premiums/"
            ),
            views.QuotationInsuranceVehiclePremiumsFormView.as_view(),
            name="create_premiums",
        ),
        path(
            "customer/<int:customer_id>/vehicle/<int:vehicle_id>/",
            views.QuotationInsuranceVehicleInsuredAmountCreateView.as_view(),
            name="insured_amount",
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
            "update_vehicle/<int:vehicle_id>/",
            views.QuotationInsuranceVehicleUpdateVehicleView.as_view(),
            name="update_vehicle",
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
        path(
            "detail/<int:quotation_id>/",
            views.QuotationInsuranceVehicleDetailView.as_view(),
            name="detail",
        ),
        path(
            "report/xlsx/<int:quotation_id>/",
            views.QuotationInsuranceVehicleReportXlsxView.as_view(),
            name="report_xlsx",
        ),
    ],
    "vehicle",
)

issuance_insurance_vehicle_urlpatterns = (
    [
        path(
            "list/",
            views.IssuanceInsuranceVehicleListView.as_view(),
            name="list",
        ),
        path(
            "list_quotations/",
            views.QuotationInsuranceVehicleListView.as_view(),
            name="list_quotations",
        ),
        path(
            "quotation_premium/<int:quotation_premium_id>/create_issuance/",
            views.IssuanceInsuranceVehicleCreateIssuanceView.as_view(),
            name="create_issuance",
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

issuance_insurance_urlpatterns = (
    [path("vehicle/", include(issuance_insurance_vehicle_urlpatterns))],
    "insurance",
)

issuance_urlpatterns = (
    [path("insurance/", include(issuance_insurance_urlpatterns))],
    "issuance",
)

app_name = "rrggweb"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "<int:consultant_id>/quotation/",
        views.QuotationView.as_view(),
        name="quotation",
    ),
    path(
        "<int:consultant_id>/issuance/",
        views.IssuanceView.as_view(),
        name="issuance",
    ),
    path("<int:consultant_id>/home/", views.HomeView.as_view(), name="home"),
    path("<int:consultant_id>/quotation/", include(quotation_urlpatterns)),
    path("<int:consultant_id>/issuance/", include(issuance_urlpatterns)),
]
