from django.urls import include, path

from . import views

quotation_insurance_vehicle_urlpatterns = (
    [
        path(
            "search_customer/",
            views.QuotationInsuranceVehicleSearchCustomerView.as_view(),
            name="search_customer",
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
            "search_vehicle/customer/<int:customer_id>/",
            views.QuotationInsuranceVehicleSearchVehicleView.as_view(),
            name="search_vehicle",
        ),
        path(
            "create_vehicle/customer/<int:customer_id>/",
            views.QuotationInsuranceVehicleCreateVehicleView.as_view(),
            name="create_vehicle",
        ),
        path(
            (
                "update_vehicle/<int:vehicle_id>/customer/"
                "<int:customer_id>/<str:origin>"
            ),
            views.QuotationInsuranceVehicleUpdateVehicleView.as_view(),
            name="update_vehicle",
        ),
        path(
            (
                "define_owner/customer/<int:customer_id>/"
                "vehicle/<int:vehicle_id>/"
            ),
            views.QuotationInsuranceVehicleDefineOwnerView.as_view(),
            name="define_owner",
        ),
        path(
            (
                "create_owner/customer/<int:customer_id>/"
                "vehicle/<int:vehicle_id>/"
            ),
            views.QuotationInsuranceVehicleCreateOwnerView.as_view(),
            name="create_owner",
        ),
        path(
            "create/customer/<int:customer_id>/vehicle/<int:vehicle_id>/",
            views.QuotationInsuranceVehicleCreateView.as_view(),
            name="create",
        ),
        path(
            "<int:quotation_id>/update/",
            views.QuotationInsuranceVehicleUpdateView.as_view(),
            name="update",
        ),
        path(
            "list/",
            views.QuotationInsuranceVehicleListView.as_view(),
            name="list",
        ),
        path(
            "detail/<int:quotation_id>/",
            views.QuotationInsuranceVehicleDetailView.as_view(),
            name="detail",
        ),
        path(
            "create_premiums/quotation/<int:quotation_id>",
            views.QuotationInsuranceVehiclePremiumsFormView.as_view(),
            name="create_premiums",
        ),
        path(
            "update_premium/<int:premium_id>/",
            views.QuotationInsuranceVehiclePremiumsUpdateView.as_view(),
            name="update_premium",
        ),
        path(
            "report/xlsx/<int:quotation_id>/",
            views.QuotationInsuranceVehicleReportXlsxView.as_view(),
            name="report_xlsx",
        ),
        path(
            "report/pdf/<int:quotation_id>/",
            views.QuotationInsuranceVehicleReportPdfView.as_view(),
            name="report_pdf",
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
        path(
            "detail/<int:issuance_id>/",
            views.IssuanceInsuranceVehicleDetailIssuanceView.as_view(),
            name="detail",
        ),
        path(
            "update/<int:issuance_id>/",
            views.IssuanceInsuranceVehicleUpdateIssuanceView.as_view(),
            name="update",
        ),
        path(
            "create_document/<int:issuance_id>/",
            views.IssuanceInsuranceVehicleAddDocumentCreateView.as_view(),
            name="create_document",
        ),
        path(
            "delete_document/<int:document_id>/issuance/<int:issuance_id>/",
            views.IssuanceInsuranceVehicleDeleteDocumentView.as_view(),
            name="delete_document",
        ),
    ],
    "vehicle",
)

issuance_insurance_urlpatterns = (
    [path("vehicle/", include(issuance_insurance_vehicle_urlpatterns))],
    "insurance",
)

issuance_urlpatterns = (
    [path("insurance/", include(issuance_insurance_urlpatterns))],
    "issuance",
)


collection_insurance_vehicle_urlpatterns = (
    [
        path(
            "list/",
            views.CollectionInsuranceVehicleListView.as_view(),
            name="list",
        ),
        path(
            "list_emissions/",
            views.IssuanceInsuranceVehicleListView.as_view(),
            name="list_emissions",
        ),
        path(
            "issuance/<int:issuance_id>/create_collection/",
            views.CollectionInsuranceVehicleCreateCollectionView.as_view(),
            name="create_collection",
        ),
    ],
    "vehicle",
)

collection_insurance_urlpatterns = (
    [path("vehicle/", include(collection_insurance_vehicle_urlpatterns))],
    "insurance",
)

collection_urlpatterns = (
    [path("insurance/", include(collection_insurance_urlpatterns))],
    "collection",
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
    path(
        "<int:consultant_id>/collection/",
        views.CollectionView.as_view(),
        name="collection",
    ),
    path("<int:consultant_id>/home/", views.HomeView.as_view(), name="home"),
    path("<int:consultant_id>/quotation/", include(quotation_urlpatterns)),
    path("<int:consultant_id>/issuance/", include(issuance_urlpatterns)),
    path("<int:consultant_id>/collection/", include(collection_urlpatterns)),
]
