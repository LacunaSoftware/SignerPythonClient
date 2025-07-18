# coding: utf-8

# flake8: noqa

"""
    Dropsigner (HML)

    <!--------------------------------------------------------------------------------------------------------------------->  <h2>Authentication</h2>  <p>  In order to call this APIs, you will need an <strong>API key</strong>. Set the API key in the header <span class=\"code\">X-Api-Key</span>: </p>  <pre>X-Api-Key: your-app|xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx</pre>  <!---------------------------------------------------------------------------------------------------------------------> <br />  <h2>HTTP Codes</h2>  <p>  The APIs will return the following HTTP codes: </p>  <table>  <thead>   <tr>    <th>Code</th>    <th>Description</th>   </tr>  </thead>  <tbody>   <tr>    <td><strong class=\"model-title\">200 (OK)</strong></td>    <td>Request processed successfully. The response is different for each API, please refer to the operation's documentation</td>   </tr>   <tr>    <td><strong class=\"model-title\">400 (Bad Request)</strong></td>    <td>Syntax error. For instance, when a required field was not provided</td>   </tr>   <tr>    <td><strong class=\"model-title\">401 (Unauthorized)</strong></td>    <td>API key not provided or invalid</td>   </tr>   <tr>    <td><strong class=\"model-title\">403 (Forbidden)</strong></td>    <td>API key is valid, but the application has insufficient permissions to complete the requested operation</td>   </tr>   <tr>    <td><strong class=\"model-title\">422 (Unprocessable Entity)</strong></td>    <td>API error. The response is as defined in <a href=\"#model-ErrorModel\">ErrorModel</a></td>   </tr>  </tbody> </table>  <br />  <h3>Error Codes</h3>  <p>Some of the error codes returned in a 422 response are provided bellow*:</p>  <ul>  <li>CertificateNotFound</li>  <li>DocumentNotFound</li>  <li>FolderNotFound</li>  <li>CpfMismatch</li>  <li>CpfNotExpected</li>  <li>InvalidFlowAction</li>  <li>DocumentInvalidKey</li> </ul>  <p style=\"font-size: 0.9em\">  *The codes shown above are the main error codes. Nonetheless, this list is not comprehensive. New codes may be added anytime without previous warning. </p>  <!--------------------------------------------------------------------------------------------------------------------->  <br />  <h2>Webhooks</h2>  <p>  It is recomended to subscribe to Webhook events <strong>instead</strong> of polling APIs. To do so, enable webhooks and register an URL that will receive a POST request  whenever one of the events bellow occur. </p> <p>  All requests have the format described in <a href=\"#model-Webhooks.WebhookModel\">Webhooks.WebhookModel</a>.  The data field varies according to the webhook event type: </p>   <table>  <thead>   <tr>    <th>Event type</th>    <th>Description</th>    <th>Payload</th>   </tr>  </thead>  <tbody>   <tr>    <td><strong class=\"model-title\">DocumentSigned</strong></td>    <td>Triggered when a document is signed.</td>    <td><a href=\"#model-Webhooks.DocumentSignedModel\">Webhooks.DocumentSignedModel</a></td>   </tr>   <tr>    <td><strong class=\"model-title\">DocumentApproved</strong></td>    <td>Triggered when a document is approved.</td>    <td><a href=\"#model-Webhooks.DocumentApprovedModel\">Webhooks.DocumentApprovedModel</a></td>   </tr>   <tr>    <td><strong class=\"model-title\">DocumentRefused</strong></td>    <td>Triggered when a document is refused.</td>    <td><a href=\"#model-Webhooks.DocumentRefusedModel\">Webhooks.DocumentRefusedModel</a></td>   </tr>   <tr>    <td><strong class=\"model-title\">DocumentConcluded</strong></td>    <td>Triggered when the flow of a document is concluded.</td>    <td><a href=\"#model-Webhooks.DocumentConcludedModel\">Webhooks.DocumentConcludedModel</a></td>   </tr>   <tr>    <td><strong class=\"model-title\">DocumentCanceled</strong></td>    <td>Triggered when the document is canceled.</td>    <td><a href=\"#model-Webhooks.DocumentCanceledModel\">Webhooks.DocumentCanceledModel</a></td>   </tr>   <tr>    <td><strong class=\"model-title\">DocumentExpired (v1.33.0)</strong></td>    <td>Triggered when the document is expired.</td>    <td><a href=\"#model-Webhooks.DocumentExpiredModel\">Webhooks.DocumentExpiredModel</a></td>   </tr>   <tr>    <td><strong class=\"model-title\">DocumentsCreated (v1.50.0)</strong></td>    <td>Triggered when one or more documents are created.</td>    <td><a href=\"#model-Webhooks.DocumentsCreatedModel\">Webhooks.DocumentsCreatedModel</a></td>   </tr>   <tr>    <td><strong class=\"model-title\">DocumentsDeleted (v1.78.0)</strong></td>    <td>Triggered when one or more documents are deleted.</td>    <td><a href=\"#model-Webhooks.DocumentsDeletedModel\">Webhooks.DocumentsDeletedModel</a></td>   </tr>  </tbody> </table>  <p>  To register your application URL and enable Webhooks, access the integrations section in your <a href=\"/private/organizations\" target=\"_blank\">organization's details page</a>. </p>   # noqa: E501

    OpenAPI spec version: 2.1.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

# import apis into sdk package
from signer_client.api.documents_api import DocumentsApi
from signer_client.api.flows_api import FlowsApi
from signer_client.api.folders_api import FoldersApi
from signer_client.api.marks_sessions_api import MarksSessionsApi
from signer_client.api.notifications_api import NotificationsApi
from signer_client.api.organizations_api import OrganizationsApi
from signer_client.api.upload_api import UploadApi
# import ApiClient
from signer_client.api_client import ApiClient
from signer_client.configuration import Configuration
# import models into sdk package
from signer_client.models.action_status import ActionStatus
from signer_client.models.agent_types import AgentTypes
from signer_client.models.agents_agent_model import AgentsAgentModel
from signer_client.models.api_uploads_body import ApiUploadsBody
from signer_client.models.applications_application_display_model import ApplicationsApplicationDisplayModel
from signer_client.models.attachments_attachment_model import AttachmentsAttachmentModel
from signer_client.models.attachments_attachment_upload_model import AttachmentsAttachmentUploadModel
from signer_client.models.attachments_create_attachment_result import AttachmentsCreateAttachmentResult
from signer_client.models.authentication_types import AuthenticationTypes
from signer_client.models.batch_item_result_model import BatchItemResultModel
from signer_client.models.billing_billing_information_model import BillingBillingInformationModel
from signer_client.models.billing_company_billing_information_model import BillingCompanyBillingInformationModel
from signer_client.models.billing_individual_billing_information_model import BillingIndividualBillingInformationModel
from signer_client.models.billing_information_types import BillingInformationTypes
from signer_client.models.certificate_holder_types import CertificateHolderTypes
from signer_client.models.certificate_types import CertificateTypes
from signer_client.models.certificates_attribute_certificate_info_model import CertificatesAttributeCertificateInfoModel
from signer_client.models.delete_action import DeleteAction
from signer_client.models.document_download_types import DocumentDownloadTypes
from signer_client.models.document_filter_status import DocumentFilterStatus
from signer_client.models.document_flows_document_flow_create_request import DocumentFlowsDocumentFlowCreateRequest
from signer_client.models.document_flows_document_flow_data import DocumentFlowsDocumentFlowData
from signer_client.models.document_flows_document_flow_details_model import DocumentFlowsDocumentFlowDetailsModel
from signer_client.models.document_flows_document_flow_model import DocumentFlowsDocumentFlowModel
from signer_client.models.document_mark_document_mark_position_model import DocumentMarkDocumentMarkPositionModel
from signer_client.models.document_mark_flow_action_position_model import DocumentMarkFlowActionPositionModel
from signer_client.models.document_mark_marks_session_create_request import DocumentMarkMarksSessionCreateRequest
from signer_client.models.document_mark_marks_session_create_response import DocumentMarkMarksSessionCreateResponse
from signer_client.models.document_mark_marks_session_model import DocumentMarkMarksSessionModel
from signer_client.models.document_mark_pre_positioned_document_mark_model import DocumentMarkPrePositionedDocumentMarkModel
from signer_client.models.document_mark_type import DocumentMarkType
from signer_client.models.document_mark_upload_ticket_model import DocumentMarkUploadTicketModel
from signer_client.models.document_query_types import DocumentQueryTypes
from signer_client.models.document_status import DocumentStatus
from signer_client.models.document_ticket_type import DocumentTicketType
from signer_client.models.document_types import DocumentTypes
from signer_client.models.documents_action_url_request import DocumentsActionUrlRequest
from signer_client.models.documents_action_url_response import DocumentsActionUrlResponse
from signer_client.models.documents_cancel_document_request import DocumentsCancelDocumentRequest
from signer_client.models.documents_create_document_request import DocumentsCreateDocumentRequest
from signer_client.models.documents_create_document_result import DocumentsCreateDocumentResult
from signer_client.models.documents_creator_model import DocumentsCreatorModel
from signer_client.models.documents_document_add_version_request import DocumentsDocumentAddVersionRequest
from signer_client.models.documents_document_additional_info_data import DocumentsDocumentAdditionalInfoData
from signer_client.models.documents_document_content_model import DocumentsDocumentContentModel
from signer_client.models.documents_document_file_model import DocumentsDocumentFileModel
from signer_client.models.documents_document_flow_edit_request import DocumentsDocumentFlowEditRequest
from signer_client.models.documents_document_list_model import DocumentsDocumentListModel
from signer_client.models.documents_document_model import DocumentsDocumentModel
from signer_client.models.documents_document_notified_emails_edit_request import DocumentsDocumentNotifiedEmailsEditRequest
from signer_client.models.documents_document_permissions_model import DocumentsDocumentPermissionsModel
from signer_client.models.documents_document_signatures_info_model import DocumentsDocumentSignaturesInfoModel
from signer_client.models.documents_document_tag_data import DocumentsDocumentTagData
from signer_client.models.documents_document_tag_model import DocumentsDocumentTagModel
from signer_client.models.documents_envelope_add_version_request import DocumentsEnvelopeAddVersionRequest
from signer_client.models.documents_flow_action_pending_model import DocumentsFlowActionPendingModel
from signer_client.models.documents_move_document_batch_request import DocumentsMoveDocumentBatchRequest
from signer_client.models.documents_move_document_request import DocumentsMoveDocumentRequest
from signer_client.models.documents_pre_positioned_mark_model import DocumentsPrePositionedMarkModel
from signer_client.models.error_model import ErrorModel
from signer_client.models.file_model import FileModel
from signer_client.models.file_upload_model import FileUploadModel
from signer_client.models.flow_action_type import FlowActionType
from signer_client.models.flow_actions_approval_model import FlowActionsApprovalModel
from signer_client.models.flow_actions_document_flow_edit_response import FlowActionsDocumentFlowEditResponse
from signer_client.models.flow_actions_flow_action_create_model import FlowActionsFlowActionCreateModel
from signer_client.models.flow_actions_flow_action_edit_model import FlowActionsFlowActionEditModel
from signer_client.models.flow_actions_flow_action_model import FlowActionsFlowActionModel
from signer_client.models.flow_actions_pending_action_model import FlowActionsPendingActionModel
from signer_client.models.flow_actions_rectified_participant_model import FlowActionsRectifiedParticipantModel
from signer_client.models.flow_actions_sign_rule_user_edit_model import FlowActionsSignRuleUserEditModel
from signer_client.models.flow_actions_sign_rule_user_model import FlowActionsSignRuleUserModel
from signer_client.models.flow_actions_signature_model import FlowActionsSignatureModel
from signer_client.models.flow_actions_xades_options_model import FlowActionsXadesOptionsModel
from signer_client.models.folder_type import FolderType
from signer_client.models.folders_folder_create_request import FoldersFolderCreateRequest
from signer_client.models.folders_folder_delete_request import FoldersFolderDeleteRequest
from signer_client.models.folders_folder_info_model import FoldersFolderInfoModel
from signer_client.models.folders_folder_organization_model import FoldersFolderOrganizationModel
from signer_client.models.health_documents_health_document_data import HealthDocumentsHealthDocumentData
from signer_client.models.health_documents_health_item_model import HealthDocumentsHealthItemModel
from signer_client.models.health_documents_health_professional_model import HealthDocumentsHealthProfessionalModel
from signer_client.models.invoices_invoice_total_model import InvoicesInvoiceTotalModel
from signer_client.models.invoices_update_invoice_payment_status_request import InvoicesUpdateInvoicePaymentStatusRequest
from signer_client.models.notarization_status import NotarizationStatus
from signer_client.models.notary_types import NotaryTypes
from signer_client.models.notifications_create_flow_action_reminder_request import NotificationsCreateFlowActionReminderRequest
from signer_client.models.notifications_email_list_notification_request import NotificationsEmailListNotificationRequest
from signer_client.models.observers_observer_create_model import ObserversObserverCreateModel
from signer_client.models.observers_observer_edit_model import ObserversObserverEditModel
from signer_client.models.observers_observer_model import ObserversObserverModel
from signer_client.models.organization_type import OrganizationType
from signer_client.models.organizations_access_profile_model import OrganizationsAccessProfileModel
from signer_client.models.organizations_organization_info_model import OrganizationsOrganizationInfoModel
from signer_client.models.organizations_organization_owner_info_model import OrganizationsOrganizationOwnerInfoModel
from signer_client.models.organizations_organization_user_model import OrganizationsOrganizationUserModel
from signer_client.models.organizations_organization_user_post_request import OrganizationsOrganizationUserPostRequest
from signer_client.models.paginated_search_response_document_flows_document_flow_model import PaginatedSearchResponseDocumentFlowsDocumentFlowModel
from signer_client.models.paginated_search_response_documents_document_list_model import PaginatedSearchResponseDocumentsDocumentListModel
from signer_client.models.paginated_search_response_folders_folder_info_model import PaginatedSearchResponseFoldersFolderInfoModel
from signer_client.models.paginated_search_response_organizations_organization_user_model import PaginatedSearchResponseOrganizationsOrganizationUserModel
from signer_client.models.pagination_orders import PaginationOrders
from signer_client.models.participant_query_types import ParticipantQueryTypes
from signer_client.models.probability import Probability
from signer_client.models.refusal_refusal_model import RefusalRefusalModel
from signer_client.models.refusal_refusal_request import RefusalRefusalRequest
from signer_client.models.security_contexts_authentication_types_model import SecurityContextsAuthenticationTypesModel
from signer_client.models.security_contexts_security_context_simple_model import SecurityContextsSecurityContextSimpleModel
from signer_client.models.signature_datavalid_selfie_validation_response import SignatureDatavalidSelfieValidationResponse
from signer_client.models.signature_evidences_model import SignatureEvidencesModel
from signer_client.models.signature_geolocation_model import SignatureGeolocationModel
from signer_client.models.signature_initials_modes import SignatureInitialsModes
from signer_client.models.signature_liveness3d_authentication_model import SignatureLiveness3dAuthenticationModel
from signer_client.models.signature_pix_authentication_model import SignaturePixAuthenticationModel
from signer_client.models.signature_selfie_model import SignatureSelfieModel
from signer_client.models.signature_signatures_info_request import SignatureSignaturesInfoRequest
from signer_client.models.signature_types import SignatureTypes
from signer_client.models.signer_model import SignerModel
from signer_client.models.ticket_model import TicketModel
from signer_client.models.timestamp_model import TimestampModel
from signer_client.models.transaction_pricing_types import TransactionPricingTypes
from signer_client.models.transaction_types import TransactionTypes
from signer_client.models.transactions_price_range_model import TransactionsPriceRangeModel
from signer_client.models.transactions_transaction_price_model import TransactionsTransactionPriceModel
from signer_client.models.upload_model import UploadModel
from signer_client.models.uploads_upload_bytes_model import UploadsUploadBytesModel
from signer_client.models.uploads_upload_bytes_request import UploadsUploadBytesRequest
from signer_client.models.users_participant_user_model import UsersParticipantUserModel
from signer_client.models.validation_item_model import ValidationItemModel
from signer_client.models.validation_results_model import ValidationResultsModel
from signer_client.models.webhook_types import WebhookTypes
from signer_client.models.webhooks_document_approved_model import WebhooksDocumentApprovedModel
from signer_client.models.webhooks_document_canceled_model import WebhooksDocumentCanceledModel
from signer_client.models.webhooks_document_concluded_model import WebhooksDocumentConcludedModel
from signer_client.models.webhooks_document_expired_model import WebhooksDocumentExpiredModel
from signer_client.models.webhooks_document_information_model import WebhooksDocumentInformationModel
from signer_client.models.webhooks_document_refused_model import WebhooksDocumentRefusedModel
from signer_client.models.webhooks_document_signed_model import WebhooksDocumentSignedModel
from signer_client.models.webhooks_documents_created_model import WebhooksDocumentsCreatedModel
from signer_client.models.webhooks_documents_deleted_action import WebhooksDocumentsDeletedAction
from signer_client.models.webhooks_documents_deleted_model import WebhooksDocumentsDeletedModel
from signer_client.models.webhooks_invoice_closed_model import WebhooksInvoiceClosedModel
from signer_client.models.webhooks_webhook_model import WebhooksWebhookModel
from signer_client.models.xades_element_identifier_types import XadesElementIdentifierTypes
from signer_client.models.xades_insertion_options import XadesInsertionOptions
from signer_client.models.xades_signature_types import XadesSignatureTypes
from signer_client.models.xml_namespace_model import XmlNamespaceModel
