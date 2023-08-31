from django.urls import include, path

from . import views

quotation_insurance_vehicle_urlpatterns = (
    [
        path(
            "list/",
            views.QIVListView.as_view(),
            name="list",
        ),
        path(
            "select_role/",
            views.QIVSelectRoleFormView.as_view(),
            name="select_role",
        ),
        path(
            "select_seller/role/<int:role_id>/",
            views.QIVSelectSellerFormView.as_view(),
            name="select_seller",
        ),
        path(
            "update_seller/<int:quotation_id>/",
            views.QIVUpdateSellerView.as_view(),
            name="update_seller",
        ),
        path(
            "search_customer/seller/<int:seller_id>/",
            views.QIVSearchCustomerView.as_view(),
            name="search_customer",
        ),
        path(
            "select_customer/<int:seller_id>/",
            views.QIVSelectCustomerFormView.as_view(),
            name="select_customer",
        ),
        path(
            "create_natural_person/seller/<int:seller_id>/",
            views.QIVCreateNaturalPersonView.as_view(),
            name="create_natural_person",
        ),
        path(
            "create_legal_person/seller/<int:seller_id>/",
            views.QIVCreateLegalPersonView.as_view(),
            name="create_legal_person",
        ),
        path(
            (
                "update_natural_person/<int:natural_person_id>/"
                "quotation/<int:quotation_id>/"
            ),
            views.QIVUpdateNaturalPersonView.as_view(),
            name="update_natural_person",
        ),
        path(
            (
                "update_natural_person_step/<int:natural_person_id>/"
                "seller/<int:seller_id>/"
            ),
            views.QIVUpdateNaturalPersonStepView.as_view(),
            name="update_natural_person_step",
        ),
        path(
            (
                "update_legal_person/<int:legal_person_id>/"
                "quotation/<int:quotation_id>/"
            ),
            views.QIVUpdateLegalPersonView.as_view(),
            name="update_legal_person",
        ),
        path(
            (
                "update_legal_person_step/<int:legal_person_id>/"
                "seller/<int:seller_id>/"
            ),
            views.QIVUpdateLegalPersonStepView.as_view(),
            name="update_legal_person_step",
        ),
        path(
            (
                "search_vehicle/seller/<int:seller_id>/"
                "customer/<int:customer_id>/"
            ),
            views.QIVSearchVehicleView.as_view(),
            name="search_vehicle",
        ),
        path(
            (
                "create_vehicle/seller/<int:seller_id>/"
                "customer/<int:customer_id>/"
            ),
            views.QIVCreateVehicleView.as_view(),
            name="create_vehicle",
        ),
        path(
            "update_vehicle/<int:vehicle_id>quotation/<int:quotation_id>/",
            views.QIVUpdateVehicleView.as_view(),
            name="update_vehicle",
        ),
        path(
            (
                "update_vehicle/<int:vehicle_id>/seller/<int:seller_id>/"
                "customer/<int:customer_id>/"
            ),
            views.QIVUpdateVehicleStepView.as_view(),
            name="update_vehicle_step",
        ),
        path(
            (
                "define_owner/seller/<int:seller_id>/"
                "customer/<int:customer_id>/vehicle/<int:vehicle_id>/"
            ),
            views.QIVDefineOwnerView.as_view(),
            name="define_owner",
        ),
        path(
            (
                "search_owner/seller/<int:seller_id>/"
                "customer/<int:customer_id>/vehicle/<int:vehicle_id>/"
            ),
            views.QIVSearchOwnerView.as_view(),
            name="search_owner",
        ),
        path(
            (
                "create_owner/seller/<int:seller_id>/"
                "customer/<int:customer_id>/vehicle/<int:vehicle_id>/"
            ),
            views.QIVCreateOwnerView.as_view(),
            name="create_owner",
        ),
        path(
            "update_owner/<int:owner_id>/quotation/<int:quotation_id>/",
            views.QIVUpdateOwnerView.as_view(),
            name="update_owner",
        ),
        path(
            (
                "update_owner/<int:owner_id>/seller/<int:seller_id>/"
                "customer/<int:customer_id>/vehicle/<int:vehicle_id>/"
            ),
            views.QIVUpdateOwnerStepView.as_view(),
            name="update_owner_step",
        ),
        path(
            (
                "create/seller/<int:seller_id>/"
                "customer/<int:customer_id>/vehicle/<int:vehicle_id>/"
            ),
            views.QIVCreateView.as_view(),
            name="create",
        ),
        path(
            "update/<int:quotation_id>/",
            views.QIVUpdateView.as_view(),
            name="update",
        ),
        path(
            "update/<int:quotation_id>/premiums/",
            views.QIVUpdateStepView.as_view(),
            name="update_step",
        ),
        path(
            "detail/<int:quotation_id>/",
            views.QIVDetailView.as_view(),
            name="detail",
        ),
        path(
            "create_premiums/quotation/<int:quotation_id>",
            views.QIVPremiumsFormView.as_view(),
            name="create_premiums",
        ),
        path(
            "update_premium/<int:premium_id>/",
            views.QIVPremiumsUpdateView.as_view(),
            name="update_premium",
        ),
        path(
            "report_xlsx/<int:quotation_id>/",
            views.QIVReportXlsxView.as_view(),
            name="report_xlsx",
        ),
        path(
            "report_pdf/<int:quotation_id>/",
            views.QIVReportPdfView.as_view(),
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
            views.IIVListView.as_view(),
            name="list",
        ),
        path(
            "list_quotations/",
            views.QIVListView.as_view(),
            name="list_quotations",
        ),
        path(
            "select_role/quotation_premium/<int:quotation_premium_id>/",
            views.IIVSelectRoleFormView.as_view(),
            name="select_role",
        ),
        path(
            (
                "select_seller/quotation_premium/<int:quotation_premium_id>/"
                "role/<int:role_id>/"
            ),
            views.IIVSelectSellerFormView.as_view(),
            name="select_seller",
        ),
        path(
            (
                "select_plan/quotation_premium/<int:quotation_premium_id>/"
                "seller/<int:seller_id>/"
            ),
            views.IIVPlanFormView.as_view(),
            name="select_plan",
        ),
        path(
            (
                "create/quotation_premium/<int:quotation_premium_id>/"
                "seller/<int:seller_id>/plan/<int:plan_id>"
            ),
            views.IIVCreateView.as_view(),
            name="create",
        ),
        path(
            "detail/<int:issuance_id>/",
            views.IIVDetailIssuanceView.as_view(),
            name="detail",
        ),
        path(
            "update/<int:issuance_id>/",
            views.IIVUpdateIssuanceView.as_view(),
            name="update",
        ),
        path(
            "update_step/<int:issuance_id>/",
            views.IIVUpdateIssuanceStepView.as_view(),
            name="update_step",
        ),
        path(
            "update_status/<int:issuance_id>/",
            views.IIVUpdateStatusFormView.as_view(),
            name="update_status",
        ),
        path(
            "create_document/<int:issuance_id>/",
            views.IIVAddDocumentCreateView.as_view(),
            name="create_document",
        ),
        path(
            "delete_document/<int:document_id>/issuance/<int:issuance_id>/",
            views.IIVDeleteDocumentView.as_view(),
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
            views.IIVListView.as_view(),
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
        "<int:registrar_id>/quotation/",
        views.QuotationView.as_view(),
        name="quotation",
    ),
    path(
        "<int:registrar_id>/issuance/",
        views.IssuanceView.as_view(),
        name="issuance",
    ),
    path(
        "<int:registrar_id>/collection/",
        views.CollectionView.as_view(),
        name="collection",
    ),
    path("<int:registrar_id>/home/", views.HomeView.as_view(), name="home"),
    path("<int:registrar_id>/quotation/", include(quotation_urlpatterns)),
    path("<int:registrar_id>/issuance/", include(issuance_urlpatterns)),
    path("<int:registrar_id>/collection/", include(collection_urlpatterns)),
]
