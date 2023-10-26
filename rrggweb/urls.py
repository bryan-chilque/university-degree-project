from django.conf import settings
from django.conf.urls.static import static
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
            ("search_vehicle/seller/<int:seller_id>/" "customer/<int:customer_id>/"),
            views.QIVSearchVehicleView.as_view(),
            name="search_vehicle",
        ),
        path(
            ("create_vehicle/seller/<int:seller_id>/" "customer/<int:customer_id>/"),
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
            "create_premium/quotation/<int:quotation_id>",
            views.QIVCreatePremiumView.as_view(),
            name="create_premium",
        ),
        path(
            "update_premium/<int:premium_id>/",
            views.QIVUpdatePremiumView.as_view(),
            name="update_premium",
        ),
        path(
            "delete_premium/<int:pk>/",
            views.QIVDeletePremiumView.as_view(),
            name="delete_premium",
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
            "select_role/quotation_premium/<int:premium_id>/",
            views.IIVSelectRoleQuotationFormView.as_view(),
            name="select_role_q",
        ),
        path(
            ("select_seller/quotation_premium/<int:premium_id>/" "role/<int:role_id>/"),
            views.IIVSelectSellerQuotationView.as_view(),
            name="select_seller_q",
        ),
        # NEW SALE
        path(
            "select_role/",
            views.IIVSelectRoleNewSaleView.as_view(),
            name="select_role_ns",
        ),
        path(
            "select_seller/role/<int:role_id>/",
            views.IIVSelectSellerNewSaleView.as_view(),
            name="select_seller_ns",
        ),
        path(
            "search_customer/seller/<int:seller_id>/",
            views.IIVSearchCustomerNewSaleView.as_view(),
            name="search_customer",
        ),
        path(
            "select_customer/seller/<int:seller_id>/",
            views.IIVSelectCustomerNewSaleView.as_view(),
            name="select_customer",
        ),
        path(
            "create_natural_person/seller/<int:seller_id>/",
            views.IIVCreateNaturalPersonNewSaleView.as_view(),
            name="create_natural_person",
        ),
        path(
            "create_legal_person/seller/<int:seller_id>/",
            views.IIVCreateLegalPersonNewSaleView.as_view(),
            name="create_legal_person",
        ),
        path(
            (
                "update_natural_person_step/<int:natural_person_id>/"
                "seller/<int:seller_id>/"
            ),
            views.IIVUpdateNaturalPersonNewSaleStepView.as_view(),
            name="update_natural_person_step",
        ),
        path(
            (
                "update_natural_person/<int:natural_person_id>/"
                "quotation/<int:quotation_id>/"
            ),
            views.IIVUpdateNaturalPersonQuotationView.as_view(),
            name="update_natural_person",
        ),
        path(
            (
                "update_legal_person_step/<int:legal_person_id>/"
                "seller/<int:seller_id>/"
            ),
            views.IIVUpdateLegalPersonNewSaleStepView.as_view(),
            name="update_legal_person_step",
        ),
        path(
            (
                "update_legal_person/<int:legal_person_id>/"
                "quotation/<int:quotation_id>/"
            ),
            views.IIVUpdateLegalPersonQuotationView.as_view(),
            name="update_legal_person",
        ),
        path(
            ("search_vehicle/seller/<int:seller_id>/" "customer/<int:customer_id>/"),
            views.IIVSearchVehicleNewSaleView.as_view(),
            name="search_vehicle",
        ),
        path(
            ("create_vehicle/seller/<int:seller_id>/" "customer/<int:customer_id>/"),
            views.IIVCreateVehicleNewSaleView.as_view(),
            name="create_vehicle",
        ),
        path(
            (
                "update_vehicle/<int:vehicle_id>/seller/"
                "<int:seller_id>/customer/<int:customer_id>/"
            ),
            views.IIVUpdateVehicleNewSaleStepView.as_view(),
            name="update_vehicle_step",
        ),
        path(
            "update_vehicle/<int:vehicle_id>/quotation/<int:quotation_id>/",
            views.IIVUpdateVehicleQuotationView.as_view(),
            name="update_vehicle",
        ),
        path(
            (
                "define_owner/seller/<int:seller_id>/"
                "customer/<int:customer_id>/vehicle/<int:vehicle_id>/"
            ),
            views.IIVDefineOwnerNewSaleView.as_view(),
            name="define_owner",
        ),
        path(
            (
                "search_owner/seller/<int:seller_id>/customer/"
                "<int:customer_id>/vehicle/<int:vehicle_id>/"
            ),
            views.IIVSearchOwnerNewSaleView.as_view(),
            name="search_owner",
        ),
        path(
            (
                "create_owner/seller/<int:seller_id>/customer/"
                "<int:customer_id>/vehicle/<int:vehicle_id>/"
            ),
            views.IIVCreateOwnerNewSaleView.as_view(),
            name="create_owner",
        ),
        path(
            (
                "update_owner/<int:owner_id>/seller/<int:seller_id>/customer/"
                "<int:customer_id>/vehicle/<int:vehicle_id>/"
            ),
            views.IIVUpdateOwnerNewSaleStepView.as_view(),
            name="update_owner_step",
        ),
        path(
            "update_owner/<int:owner_id>/quotation/<int:quotation_id>/",
            views.IIVUpdateOwnerQuotationView.as_view(),
            name="update_owner",
        ),
        path(
            (
                "create_quotation_ns/seller/<int:seller_id>/customer/"
                "<int:customer_id>/vehicle/<int:vehicle_id>/"
            ),
            views.IIVCreateQuotationNewSaleView.as_view(),
            name="create_quotation_ns",
        ),
        path(
            "update_quotation_step/<int:quotation_id>/seller/<int:seller_id>/",
            views.IIVUpdateQuotationStepNewSaleView.as_view(),
            name="update_quotation_step",
        ),
        path(
            "update_quotation/<int:quotation_id>/",
            views.IIVUpdateQuotationView.as_view(),
            name="update_quotation",
        ),
        path(
            ("create_premium/seller/<int:seller_id>/" "quotation/<int:quotation_id>/"),
            views.IIVCreatePremiumNewSaleView.as_view(),
            name="create_premium",
        ),
        path(
            "update_premium_step/<int:premium_id>/seller/<int:seller_id>/",
            views.IIVUpdatePremiumStepNewSaleView.as_view(),
            name="update_premium_step",
        ),
        path(
            "select_plan_q/premium/<int:premium_id>/seller/<int:seller_id>/",
            views.IIVSelectPlanQuotationView.as_view(),
            name="select_plan_q",
        ),
        path(
            "select_plan_ns/premium/<int:premium_id>/seller/<int:seller_id>/",
            views.IIVSelectPlanNewSaleView.as_view(),
            name="select_plan_ns",
        ),
        path(
            (
                "create_step_q/premium/<int:premium_id>/"
                "seller/<int:seller_id>/plan/<int:plan_id>"
            ),
            views.IIVCreateStepQuotationView.as_view(),
            name="create_step_q",
        ),
        path(
            (
                "create_step_ns/premium/<int:premium_id>/"
                "seller/<int:seller_id>/plan/<int:plan_id>"
            ),
            views.IIVCreateStepNewSaleView.as_view(),
            name="create_step_ns",
        ),
        path(
            "detail/<int:issuance_id>/",
            views.IIVDetailView.as_view(),
            name="detail",
        ),
        path(
            "update_step_q/<int:issuance_id>/",
            views.IIVUpdateStepQuotationView.as_view(),
            name="update_step_q",
        ),
        path(
            "update_step_ns/<int:issuance_id>/",
            views.IIVUpdateStepNewSaleView.as_view(),
            name="update_step_ns",
        ),
        path(
            "create_document_q/<int:issuance_id>/",
            views.IIVAddDocumentQuotationStepView.as_view(),
            name="create_document_q",
        ),
        path(
            "create_document_ns/<int:issuance_id>/",
            views.IIVAddDocumentNewSaleView.as_view(),
            name="create_document_ns",
        ),
        path(
            "create_document_ed/<int:issuance_id>/",
            views.IIVAddDocumentDetailView.as_view(),
            name="create_document_ed",
        ),
        path(
            "get_document/<int:document_id>/",
            views.GetDocumentView.as_view(),
            name="get_document",
        ),
        path(
            "delete_document_q/<int:document_id>/issuance/<int:issuance_id>/",
            views.IIVDeleteDocumentQuotationStepView.as_view(),
            name="delete_document_q",
        ),
        path(
            "delete_document_ns/<int:document_id>/issuance/<int:issuance_id>/",
            views.IIVDeleteDocumentNewSaleView.as_view(),
            name="delete_document_ns",
        ),
        path(
            "delete_document_ed/<int:document_id>/issuance/<int:issuance_id>/",
            views.IIVDeleteDocumentDetailView.as_view(),
            name="delete_document_ed",
        ),
        path(
            "update/<int:issuance_id>/",
            views.IIVUpdateIssuanceView.as_view(),
            name="update",
        ),
        path(
            "update_status/<int:issuance_id>/",
            views.IIVUpdateStatusDetailView.as_view(),
            name="update_status",
        ),
        path(
            "list_renewal/",
            views.IIVRenewalListView.as_view(),
            name="list_renewal",
        ),
        # RENEWAL 1
        path(
            "select_role_nr/",
            views.IIVSelectRoleNewRenewalView.as_view(),
            name="select_role_nr",
        ),
        path(
            "select_seller_nr/role/<int:role_id>/",
            views.IIVSelectSellerNewRenewalView.as_view(),
            name="select_seller_nr",
        ),
        path(
            "search_customer_nr/seller/<int:seller_id>/",
            views.IIVSearchCustomerNewRenewalView.as_view(),
            name="search_customer_nr",
        ),
        path(
            "select_customer_nr/seller/<int:seller_id>/",
            views.IIVSelectCustomerNewRenewalView.as_view(),
            name="select_customer_nr",
        ),
        path(
            "create_natural_person_nr/seller/<int:seller_id>/",
            views.IIVCreateNaturalPersonNewRenewalView.as_view(),
            name="create_natural_person_nr",
        ),
        path(
            "create_legal_person_nr/seller/<int:seller_id>/",
            views.IIVCreateLegalPersonNewRenewalView.as_view(),
            name="create_legal_person_nr",
        ),
        path(
            (
                "update_natural_person_step_nr/<int:natural_person_id>/"
                "seller/<int:seller_id>/"
            ),
            views.IIVUpdateNaturalPersonNewRenewalStepView.as_view(),
            name="update_natural_person_step_nr",
        ),
        path(
            (
                "update_legal_person_step_nr/<int:legal_person_id>/"
                "seller/<int:seller_id>/"
            ),
            views.IIVUpdateLegalPersonNewRenewalStepView.as_view(),
            name="update_legal_person_step_nr",
        ),
        path(
            ("search_vehicle_nr/seller/<int:seller_id>/" "customer/<int:customer_id>/"),
            views.IIVSearchVehicleNewRenewalView.as_view(),
            name="search_vehicle_nr",
        ),
        path(
            ("create_vehicle_nr/seller/<int:seller_id>/" "customer/<int:customer_id>/"),
            views.IIVCreateVehicleNewRenewalView.as_view(),
            name="create_vehicle_nr",
        ),
        path(
            (
                "update_vehicle_nr/<int:vehicle_id>/seller/"
                "<int:seller_id>/customer/<int:customer_id>/"
            ),
            views.IIVUpdateVehicleNewRenewalStepView.as_view(),
            name="update_vehicle_step_nr",
        ),
        path(
            (
                "define_owner_nr/seller/<int:seller_id>/"
                "customer/<int:customer_id>/vehicle/<int:vehicle_id>/"
            ),
            views.IIVDefineOwnerNewRenewalView.as_view(),
            name="define_owner_nr",
        ),
        path(
            (
                "search_owner_nr/seller/<int:seller_id>/customer/"
                "<int:customer_id>/vehicle/<int:vehicle_id>/"
            ),
            views.IIVSearchOwnerNewRenewalView.as_view(),
            name="search_owner_nr",
        ),
        path(
            (
                "create_owner_nr/seller/<int:seller_id>/customer/"
                "<int:customer_id>/vehicle/<int:vehicle_id>/"
            ),
            views.IIVCreateOwnerNewRenewalView.as_view(),
            name="create_owner_nr",
        ),
        path(
            (
                "update_owner_nr/<int:owner_id>/seller/<int:seller_id>/"
                "customer/<int:customer_id>/vehicle/<int:vehicle_id>/"
            ),
            views.IIVUpdateOwnerNewRenewalStepView.as_view(),
            name="update_owner_step_nr",
        ),
        path(
            (
                "create_quotation_nr/seller/<int:seller_id>/customer/"
                "<int:customer_id>/vehicle/<int:vehicle_id>/"
            ),
            views.IIVCreateQuotationNewRenewalView.as_view(),
            name="create_quotation_nr",
        ),
        path(
            ("update_quotation_step_nr/<int:quotation_id>/" "seller/<int:seller_id>/"),
            views.IIVUpdateQuotationStepNewRenewalView.as_view(),
            name="update_quotation_step_nr",
        ),
        path(
            (
                "create_premium_nr/seller/<int:seller_id>/"
                "quotation/<int:quotation_id>/"
            ),
            views.IIVCreatePremiumNewRenewalView.as_view(),
            name="create_premium_nr",
        ),
        path(
            "update_premium_step_nr/<int:premium_id>/seller/<int:seller_id>/",
            views.IIVUpdatePremiumStepNewRenewalView.as_view(),
            name="update_premium_step_nr",
        ),
        path(
            "select_plan_nr/premium/<int:premium_id>/seller/<int:seller_id>/",
            views.IIVSelectPlanNewRenewalView.as_view(),
            name="select_plan_nr",
        ),
        path(
            (
                "create_step_nr/premium/<int:premium_id>/"
                "seller/<int:seller_id>/plan/<int:plan_id>"
            ),
            views.IIVCreateStepNewRenewalView.as_view(),
            name="create_step_nr",
        ),
        path(
            "update_step_nr/<int:issuance_id>/",
            views.IIVUpdateStepNewRenewalView.as_view(),
            name="update_step_nr",
        ),
        path(
            "create_document_nr/<int:issuance_id>/",
            views.IIVAddDocumentNewRenewalView.as_view(),
            name="create_document_nr",
        ),
        path(
            "delete_document_nr/<int:document_id>/issuance/<int:issuance_id>/",
            views.IIVDeleteDocumentNewRenewalView.as_view(),
            name="delete_document_nr",
        ),
        # RENEWAL 2
        path(
            "create_quotation_r/emission/<int:issuance_id>/",
            views.IIVCreateQuotationRenewalView.as_view(),
            name="create_quotation_r",
        ),
        path(
            ("update_quotation_step/<int:quotation_id>/" "issuance/<int:issuance_id>/"),
            views.IIVUpdateQuotationStepRenewalView.as_view(),
            name="update_quotation_step",
        ),
        path(
            (
                "create_premium/issuance/<int:issuance_id>/"
                "quotation/<int:quotation_id>/"
            ),
            views.IIVCreatePremiumRenewalView.as_view(),
            name="create_premium",
        ),
        path(
            "update_premium_step/<int:premium_id>/issuance/<int:issuance_id>/",
            views.IIVUpdatePremiumStepRenewalView.as_view(),
            name="update_premium_step",
        ),
        path(
            (
                "update_natural_person/<int:natural_person_id>/"
                "issuance/<int:issuance_id>/premium/<int:premium_id>/"
                "seller/<int:seller_id>/"
            ),
            views.IIVUpdateNaturalPersonRenewalView.as_view(),
            name="update_natural_person",
        ),
        path(
            (
                "update_legal_person/<int:legal_person_id>/"
                "issuance/<int:issuance_id>/premium/<int:premium_id>/"
                "seller/<int:seller_id>/"
            ),
            views.IIVUpdateLegalPersonRenewalView.as_view(),
            name="update_legal_person",
        ),
        path(
            (
                "update_vehicle/<int:vehicle_id>/"
                "issuance/<int:issuance_id>/premium/<int:premium_id>/"
                "seller/<int:seller_id>/"
            ),
            views.IIVUpdateVehicleRenewalView.as_view(),
            name="update_vehicle",
        ),
        path(
            (
                "update_owner/<int:owner_id>/"
                "issuance/<int:issuance_id>/premium/<int:premium_id>/"
                "seller/<int:seller_id>/"
            ),
            views.IIVUpdateOwnerRenewalView.as_view(),
            name="update_owner",
        ),
        path(
            (
                "change_seller_r/<int:seller_id>"
                "issuance/<int:issuance_id>/premium/<int:premium_id>/"
            ),
            views.IIVChangeSellerRenewalView.as_view(),
            name="change_seller_r",
        ),
        path(
            (
                "create_step_r/issuance/<int:issuance_id>/"
                "premium/<int:premium_id>/seller/<int:seller_id>"
            ),
            views.IIVCreateStepRenewalView.as_view(),
            name="create_step_r",
        ),
        path(
            "update_step_r/<int:issuance_id>/",
            views.IIVUpdateIssuanceStepRenewalView.as_view(),
            name="update_step_r",
        ),
        path(
            "create_document_r/<int:issuance_id>/",
            views.IIVCreateDocumentRenewalView.as_view(),
            name="create_document_r",
        ),
        path(
            "delete_document_r/<int:document_id>/issuance/<int:issuance_id>/",
            views.IIVDeleteDocumentRenewalView.as_view(),
            name="delete_document_r",
        ),
        path(
            "create_endorsement/<int:issuance_id>/",
            views.IIVCreateEndorsementDetailView.as_view(),
            name="create_endorsement",
        ),
        path(
            "endorsement_detail/<int:pk>/issuance/<int:issuance_id>/",
            views.IIVDetailEndorsementView.as_view(),
            name="endorsement_detail",
        ),
        path(
            ("update_endorsement/<int:endorsement_id>/" "issuance/<int:issuance_id>/"),
            views.IIVUpdateEndorsementView.as_view(),
            name="update_endorsement",
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
            views.CMSelectCustomerFormView.as_view(),
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
            views.CMChangeAssociateConsultantView.as_view(),
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
    path(
        "<int:registrar_id>/historical-data/",
        views.HistoricalDataListView.as_view(),
        name="historical_data_list",
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

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
