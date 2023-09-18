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
                "update_natural_person_step/<int:natural_person_id>/"
                "seller/<int:seller_id>/"
            ),
            views.QIVUpdateNaturalPersonStepView.as_view(),
            name="update_natural_person_step",
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
            (
                "update_vehicle/<int:vehicle_id>/seller/<int:seller_id>/"
                "customer/<int:customer_id>/"
            ),
            views.QIVUpdateVehicleStepView.as_view(),
            name="update_vehicle_step",
        ),
        path(
            "update_vehicle/<int:vehicle_id>quotation/<int:quotation_id>/",
            views.QIVUpdateVehicleView.as_view(),
            name="update_vehicle",
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
            (
                "update_owner/<int:owner_id>/seller/<int:seller_id>/"
                "customer/<int:customer_id>/vehicle/<int:vehicle_id>/"
            ),
            views.QIVUpdateOwnerStepView.as_view(),
            name="update_owner_step",
        ),
        path(
            "update_owner/<int:owner_id>/quotation/<int:quotation_id>/",
            views.QIVUpdateOwnerView.as_view(),
            name="update_owner",
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
            "update/<int:quotation_id>/premiums/",
            views.QIVUpdateStepView.as_view(),
            name="update_step",
        ),
        path(
            "update/<int:quotation_id>/",
            views.QIVUpdateView.as_view(),
            name="update",
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
            "define_record_type/",
            views.IIVDefineRegistrationTypeView.as_view(),
            name="define_record_type",
        ),
        path(
            "define_new_sale/",
            views.IIVDefineNewSaleView.as_view(),
            name="define_new_sale",
        ),
        path(
            "list_quotations/",
            views.IIVListQuotationView.as_view(),
            name="list_quotations",
        ),
        path(
            "quotation_detail/<int:quotation_id>/",
            views.IIVQuotationDetailView.as_view(),
            name="quotation_detail",
        ),
        path(
            "select_role/",
            views.IIVSelectRoleNSFormView.as_view(),
            name="select_role_ns",
        ),
        path(
            "select_seller/role/<int:role_id>/",
            views.IIVSelectSellerNSFormView.as_view(),
            name="select_seller_ns",
        ),
        path(
            "select_role/quotation_premium/<int:premium_id>/",
            views.IIVSelectRoleQFormView.as_view(),
            name="select_role_q",
        ),
        path(
            (
                "select_seller/quotation_premium/<int:premium_id>/"
                "role/<int:role_id>/"
            ),
            views.IIVSelectSellerQFormView.as_view(),
            name="select_seller_q",
        ),
        # NEW SALE
        path(
            "search_customer/seller/<int:seller_id>/",
            views.IIVSearchCustomerView.as_view(),
            name="search_customer",
        ),
        path(
            "select_customer/seller/<int:seller_id>/",
            views.IIVSelectCustomerFormView.as_view(),
            name="select_customer",
        ),
        path(
            "create_natural_person/seller/<int:seller_id>/",
            views.IIVCreateNaturalPersonView.as_view(),
            name="create_natural_person",
        ),
        path(
            "create_legal_person/seller/<int:seller_id>/",
            views.IIVCreateLegalPersonView.as_view(),
            name="create_legal_person",
        ),
        path(
            (
                "update_natural_person_step/<int:natural_person_id>/"
                "seller/<int:seller_id>/"
            ),
            views.IIVUpdateNaturalPersonStepView.as_view(),
            name="update_natural_person_step",
        ),
        path(
            (
                "update_natural_person/<int:natural_person_id>/"
                "quotation/<int:quotation_id>/"
            ),
            views.IIVUpdateNaturalPersonQView.as_view(),
            name="update_natural_person",
        ),
        path(
            (
                "update_legal_person_step/<int:legal_person_id>/"
                "seller/<int:seller_id>/"
            ),
            views.IIVUpdateLegalPersonStepView.as_view(),
            name="update_legal_person_step",
        ),
        path(
            (
                "update_legal_person/<int:legal_person_id>/"
                "quotation/<int:quotation_id>/"
            ),
            views.IIVUpdateLegalPersonQView.as_view(),
            name="update_legal_person",
        ),
        path(
            (
                "search_vehicle/seller/<int:seller_id>/"
                "customer/<int:customer_id>/"
            ),
            views.IIVSearchVehicleView.as_view(),
            name="search_vehicle",
        ),
        path(
            (
                "create_vehicle/seller/<int:seller_id>/"
                "customer/<int:customer_id>/"
            ),
            views.IIVCreateVehicleView.as_view(),
            name="create_vehicle",
        ),
        path(
            (
                "update_vehicle/<int:vehicle_id>/seller/"
                "<int:seller_id>/customer/<int:customer_id>/"
            ),
            views.IIVUpdateVehicleStepView.as_view(),
            name="update_vehicle_step",
        ),
        path(
            "update_vehicle/<int:vehicle_id>//quotation/<int:quotation_id>/",
            views.IIVUpdateVehicleQView.as_view(),
            name="update_vehicle",
        ),
        path(
            (
                "define_owner/seller/<int:seller_id>/"
                "customer/<int:customer_id>/vehicle/<int:vehicle_id>/"
            ),
            views.IIVDefineOwnerView.as_view(),
            name="define_owner",
        ),
        path(
            (
                "search_owner/seller/<int:seller_id>/customer/"
                "<int:customer_id>/vehicle/<int:vehicle_id>/"
            ),
            views.IIVSearchOwnerView.as_view(),
            name="search_owner",
        ),
        path(
            (
                "create_owner/seller/<int:seller_id>/customer/"
                "<int:customer_id>/vehicle/<int:vehicle_id>/"
            ),
            views.IIVCreateOwnerView.as_view(),
            name="create_owner",
        ),
        path(
            (
                "update_owner/<int:owner_id>/seller/<int:seller_id>/customer/"
                "<int:customer_id>/vehicle/<int:vehicle_id>/"
            ),
            views.IIVUpdateOwnerStepView.as_view(),
            name="update_owner_step",
        ),
        path(
            "update_owner/<int:owner_id>/quotation/<int:quotation_id>/",
            views.IIVUpdateOwnerQView.as_view(),
            name="update_owner",
        ),
        path(
            (
                "create_quotation/seller/<int:seller_id>/customer/"
                "<int:customer_id>/vehicle/<int:vehicle_id>/"
            ),
            views.IIVCreateQuotationView.as_view(),
            name="create_quotation",
        ),
        path(
            "update_quotation/<int:quotation_id>/seller/<int:seller_id>/",
            views.IIVUpdateQuotationStepView.as_view(),
            name="update_quotation_step",
        ),
        path(
            "update_quotation/<int:quotation_id>/",
            views.IIVUpdateQuotationView.as_view(),
            name="update_quotation",
        ),
        path(
            (
                "create_premium/seller/<int:seller_id>/"
                "quotation/<int:quotation_id>/"
            ),
            views.IIVQuotationPremiumCreateView.as_view(),
            name="create_premium",
        ),
        path(
            "update_premium_step/<int:premium_id>/seller/<int:seller_id>/",
            views.IIVPremiumsUpdateStepView.as_view(),
            name="update_premium_step",
        ),
        path(
            "update_premium/<int:premium_id>/",
            views.IIVPremiumsUpdateQView.as_view(),
            name="update_premium",
        ),
        path(
            "select_plan_q/premium/<int:premium_id>/seller/<int:seller_id>/",
            views.IIVPlanFormQView.as_view(),
            name="select_plan_q",
        ),
        path(
            "select_plan_ns/premium/<int:premium_id>/seller/<int:seller_id>/",
            views.IIVPlanFormNSView.as_view(),
            name="select_plan_ns",
        ),
        path(
            (
                "create_step_q/premium/<int:premium_id>/"
                "seller/<int:seller_id>/plan/<int:plan_id>"
            ),
            views.IIVCreateStepQView.as_view(),
            name="create_step_q",
        ),
        path(
            (
                "create_step_ns/premium/<int:premium_id>/"
                "seller/<int:seller_id>/plan/<int:plan_id>"
            ),
            views.IIVCreateStepNSView.as_view(),
            name="create_step_ns",
        ),
        path(
            "detail/<int:issuance_id>/",
            views.IIVDetailIssuanceView.as_view(),
            name="detail",
        ),
        path(
            "update_step_q/<int:issuance_id>/",
            views.IIVUpdateIssuanceStepQView.as_view(),
            name="update_step_q",
        ),
        path(
            "update_step_ns/<int:issuance_id>/",
            views.IIVUpdateIssuanceStepNSView.as_view(),
            name="update_step_ns",
        ),
        path(
            "create_document_q/<int:issuance_id>/",
            views.IIVAddDocumentQCreateView.as_view(),
            name="create_document_q",
        ),
        path(
            "create_document_ns/<int:issuance_id>/",
            views.IIVAddDocumentNSCreateView.as_view(),
            name="create_document_ns",
        ),
        path(
            "delete_document_q/<int:document_id>/issuance/<int:issuance_id>/",
            views.IIVAddDocumentQCreateView.as_view(),
            name="delete_document_q",
        ),
        path(
            "delete_document_ns/<int:document_id>/issuance/<int:issuance_id>/",
            views.IIVDeleteDocumentNSView.as_view(),
            name="delete_document_ns",
        ),
        path(
            "update/<int:issuance_id>/",
            views.IIVUpdateIssuanceView.as_view(),
            name="update",
        ),
        path(
            "update_status/<int:issuance_id>/",
            views.IIVUpdateStatusFormView.as_view(),
            name="update_status",
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

customer_membership_urlpatterns = (
    [
        path(
            "list/",
            views.CustomerMembershipListView.as_view(),
            name="list",
        ),
        path(
            "select_role/",
            views.CMSelectRoleFormView.as_view(),
            name="select_role",
        ),
        path(
            "select_seller/role/<int:role_id>/",
            views.CMSelectSellerFormView.as_view(),
            name="select_seller",
        ),
        path(
            "select_customer/seller/<int:seller_id>/",
            views.SelectCustomerMembershipFormView.as_view(),
            name="select_customer",
        ),
        path(
            "create_natural_person/seller/<int:seller_id>/",
            views.CMCreateNaturalPersonView.as_view(),
            name="create_natural_person",
        ),
        path(
            "create_legal_person/seller/<int:seller_id>/",
            views.CMCreateLegalPersonView.as_view(),
            name="create_legal_person",
        ),
        path(
            "update_natural_person/natural_person/<int:natural_person_id>",
            views.CMUpdateNaturalPersonView.as_view(),
            name="update_natural_person",
        ),
        path(
            "update_legal_person/legal_person/<int:legal_person_id>",
            views.CMUpdateLegalPersonView.as_view(),
            name="update_legal_person",
        ),
        path(
            "delete_natural_person/natural_person/<int:pk>",
            views.CMDeleteNaturalPersonView.as_view(),
            name="delete_natural_person",
        ),
        path(
            "delete_legal_person/legal_person/<int:pk>",
            views.CMDeleteLegalPersonView.as_view(),
            name="delete_legal_person",
        ),
        path(
            "change_consultant/<int:customer_id>",
            views.CMChangeConsultantView.as_view(),
            name="change_consultant",
        ),
        path(
            "detail/<int:pk>/",
            views.CustomerMembershipDetailView.as_view(),
            name="detail",
        ),
    ],
    "customer_membership",
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
    path(
        "<int:registrar_id>/customer_membership/",
        include(customer_membership_urlpatterns),
    ),
]
