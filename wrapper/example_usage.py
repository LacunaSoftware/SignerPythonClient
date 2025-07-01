"""
Example usage of the SignerClient wrapper for the Lacuna Signer API.

This file demonstrates various operations available through the wrapper,
including document management, signature flows, folder operations, and more.
"""

import os
from signer_client.client import SignerClient, create_signer_client
from signer_client.models import (
    DocumentsCreateDocumentRequest, DocumentsCreateDocumentResult,
    DocumentsDocumentModel, DocumentsDocumentListModel,
    DocumentsDocumentFileModel, DocumentsDocumentContentModel,
    DocumentsDocumentSignaturesInfoModel, DocumentsDocumentPermissionsModel,
    DocumentsDocumentTagModel, DocumentsDocumentTagData,
    DocumentsDocumentAdditionalInfoData, DocumentsCreatorModel,
    DocumentsActionUrlRequest, DocumentsActionUrlResponse,
    DocumentsCancelDocumentRequest, DocumentsDocumentAddVersionRequest,
    DocumentsDocumentFlowEditRequest, DocumentsDocumentNotifiedEmailsEditRequest,
    DocumentsEnvelopeAddVersionRequest, DocumentsMoveDocumentRequest,
    DocumentsMoveDocumentBatchRequest, DocumentsPrePositionedMarkModel,
    DocumentsFlowActionPendingModel,
    DocumentFlowsDocumentFlowCreateRequest, DocumentFlowsDocumentFlowModel,
    DocumentFlowsDocumentFlowData, DocumentFlowsDocumentFlowDetailsModel,
    FileUploadModel,
    FoldersFolderCreateRequest, FoldersFolderInfoModel, FoldersFolderOrganizationModel,
    FoldersFolderDeleteRequest,
    UploadsUploadBytesRequest, UploadsUploadBytesModel, FileModel, UploadModel,
    FlowActionsFlowActionCreateModel, FlowActionsFlowActionModel,
    FlowActionsFlowActionEditModel, FlowActionsDocumentFlowEditResponse,
    FlowActionsApprovalModel, FlowActionsSignatureModel, FlowActionsPendingActionModel,
    FlowActionsRectifiedParticipantModel, FlowActionsSignRuleUserModel,
    FlowActionsSignRuleUserEditModel, FlowActionsXadesOptionsModel,
    UsersParticipantUserModel,
    DocumentStatus, DocumentTypes, FolderType, FlowActionType,
    SignatureTypes, AuthenticationTypes, PaginationOrders,
    DocumentDownloadTypes, DocumentTicketType, DocumentFilterStatus,
    DocumentQueryTypes, DocumentMarkType,
    NotificationsCreateFlowActionReminderRequest, NotificationsEmailListNotificationRequest,
    PaginatedSearchResponseDocumentsDocumentListModel, 
    PaginatedSearchResponseFoldersFolderInfoModel,
    PaginatedSearchResponseDocumentFlowsDocumentFlowModel,
    PaginatedSearchResponseOrganizationsOrganizationUserModel,
    OrganizationsOrganizationUserPostRequest, OrganizationsOrganizationUserModel,
    DocumentMarkMarksSessionCreateRequest, DocumentMarkMarksSessionCreateResponse,
    DocumentMarkMarksSessionModel, DocumentMarkDocumentMarkPositionModel,
    DocumentMarkFlowActionPositionModel, DocumentMarkPrePositionedDocumentMarkModel,
    DocumentMarkUploadTicketModel,
    BatchItemResultModel, TicketModel, SignatureSignaturesInfoRequest,
    RefusalRefusalRequest, RefusalRefusalModel, SignerModel,
    WebhooksDocumentSignedModel, WebhooksDocumentApprovedModel,
    WebhooksDocumentRefusedModel, WebhooksDocumentConcludedModel,
    WebhooksDocumentCanceledModel, WebhooksDocumentExpiredModel,
    WebhooksDocumentsCreatedModel, WebhooksDocumentsDeletedModel,
    WebhooksDocumentsDeletedAction, WebhooksDocumentInformationModel,
    HealthDocumentsHealthDocumentData, HealthDocumentsHealthItemModel,
    HealthDocumentsHealthProfessionalModel
)
# Configuration
API_KEY = "Teste App|fd0bad85cd9f8645b3a57cf787867800a2172bc36c6646951088181413fb750c"
BASE_URL = "https://signer-lac.azurewebsites.net"  # Use production URL for live environment

def get_document_status_simple(document_id):
    """Simple function to get document status directly."""
    client = create_signer_client(API_KEY, BASE_URL)
    try:
        status = client.get_document_status(document_id)
        return status
    finally:
        client.close()

def main():
    """Main example function demonstrating various API operations."""
    
    # Initialize the client
    client = create_signer_client(API_KEY, BASE_URL)
    
    try:
        print("=== Lacuna Signer API Examples ===\n")

        # ============================================================================
        # FILE UPLOAD OPERATIONS
        # ============================================================================
        
        file_path = "res/sample.pdf"
        print("\n\n1. File Upload Operations")
        print("-" * 50)

        # Upload file bytes
        print("\nUploading file bytes...")
        with open(file_path, "rb") as f:
            file_bytes = f.read()
        uploaded_bytes = client.upload_file_bytes(
            file_bytes=file_bytes
        )
        uploaded_bytes.file_name = "sample.pdf"
        uploaded_bytes.content_type = "application/pdf"
    
        print(f"Bytes uploaded with ID: {uploaded_bytes.id}")
        
        # ============================================================================
        # ============================================================================
        # DOCUMENT OPERATIONS
        # ============================================================================
        
        print("1. Document Operations")
        print("-" * 50)
        
        # Create a document with signature flow
        print("\nCreating a document with signature flow...")
        document = client.create_document_with_signer(
            file_upload=FileUploadModel(
                id=uploaded_bytes.id,
                name=uploaded_bytes.file_name,
                content_type=uploaded_bytes.content_type,
                display_name="Sample PDF with signature flow"
            ),
            title="Sample Contract",
            signer=UsersParticipantUserModel(
                name="Jack Bauer",
                email="jack.bauer@mailinator.com",
                identifier="75502846369"
            ),
            flow_action=FlowActionsFlowActionCreateModel(
                type=FlowActionType.SIGNER,
                user=UsersParticipantUserModel(
                    name="Jack Bauer",
                    email="jack.bauer@mailinator.com",
                    identifier="75502846369"
                ),
                title="Please review and sign this contract."
        ))
        document = document[0]
        print(f"Document created with ID: {document.document_id}")
        
        # Get document details by ID
        print("\nGetting document details...")
        document_details = client.get_document(document.document_id)
        print(f"document_details attributes: {dir(document_details)}")
        print(f"document_details as dict: {document_details.__dict__}")
        print(f"Document title: {document_details.name}")
        print(f"Document status: {document_details.status}")
        print(f"Created at: {document_details.creation_date}")
        
        # Get document content
        print("\nGetting document content...")
        content = client.get_document_content(document_details.id)
        if content is not None:
            print(f"Document content size: {len(content)} bytes")
        else:
            print("Document content is not available (None returned)")
        
        # Get document content as base64
        print("\nGetting document content as base64...")
        content_b64 = client.get_document_content_b64(document_details.id)
        if content_b64 and hasattr(content_b64, 'bytes') and content_b64.bytes is not None:
            print(f"Base64 content: {content_b64.bytes}")
            print(f"Base64 content length: {len(content_b64.bytes)}")
        else:
            print("Base64 content is not available (None returned or missing attribute)")
        
        # Get document signatures details
        # This case will be commented because the document is not signed yet
        # print("\nGetting document signatures details...")
        # try:
        #     signatures = client.get_document_signatures_details(document_details.id)
        # except Exception as e:
        #     print(f"Error getting document signatures details: {e}")
        #     signatures = None
        # if signatures is not None, print the number of signatures
        # if signatures is not None:
        #     print(f"Number of signatures: {len(signatures.signatures)}")
        # else:
        #     print("No signatures found")
        
        # Get document ticket
        print("\nGetting document ticket...")
        ticket = client.get_document_ticket(document_details.id)
        print(f"Ticket location: {getattr(ticket, 'location', None)}")
        
        # Get document status
        print("\nGetting document status...")
        # Gracefully handle a http error 422
        try:
            status = client.get_document_status(document_details.id)
            print(f"Document status: {status}")
        except Exception as e:
            print(f"Error getting document status: {e}")
            status = "Unknown"
        
        # Get document summary
        # Gracefully handle a http error 422
        try:
            print("\nGetting document summary...")
            summary = client.get_document_summary(document_details.id)
            print(f"Summary: {summary}")
        except Exception as e:
            print(f"Error getting document summary: {e}")
            summary = "Unknown"
        
        # List documents
        print("\nListing documents...")
        try:
            # Only pass non-None parameters to avoid API validation errors
            params = {"limit": 5}
            documents = client.list_documents(**params)
            if hasattr(documents, 'items') and documents.items is not None:
                print(f"Found {len(documents.items)} documents")
                if documents.items:
                    print(f"First document: {documents.items[0].name if hasattr(documents.items[0], 'name') else 'Unknown'}")
            else:
                print("No documents found or items property is None")
        except Exception as e:
            print(f"Error listing documents: {e}")
        
        # Get signing URL
        print("\nGetting signing URL...")
        try:
            # Use the actual signer email from the document
            signer_email = document_details.flow_actions[0].user.email if document_details.flow_actions else "jack.bauer@mailinator.com"
            signing_url = client.get_signing_url(document_details.id, signer_email)
            print(f"Signing URL: {signing_url}")
        except Exception as e:
            print(f"Error getting signing URL: {e}")
        
        # Create action URL
        print("\nCreating action URL...")
        try:
            # Use the actual signer email and identifier from the document
            signer_email = document_details.flow_actions[0].user.email if document_details.flow_actions else "jack.bauer@mailinator.com"
            signer_identifier = document_details.flow_actions[0].user.identifier if document_details.flow_actions else "75502846369"
            action_request = DocumentsActionUrlRequest(email_address=signer_email, identifier=signer_identifier)
            action_url = client.create_action_url(document_details.id, action_request)
            print(f"Action URL: {action_url.url}")
        except Exception as e:
            print(f"Error creating action URL: {e}")
        
        # Get signatures by key
        print("\nGetting signatures by key...")
        try:
            if hasattr(document_details, 'key') and document_details.key:
                signatures_by_key = client.get_signatures_by_key(document_details.key)
                print(f"Signatures found: {len(signatures_by_key)}")
            else:
                print("No key found for document.")
        except Exception as e:
            print(f"Error getting signatures by key: {e}")
        
        # Validate signatures
        print("\nValidating signatures...")
        try:
            validation_request = SignatureSignaturesInfoRequest(
                file_id=document_details.id,
                mime_type=document_details.mime_type
            )
            validation_result = client.validate_signatures(validation_request)
            print(f"Validation result: {validation_result}")
        except Exception as e:
            print(f"Error validating signatures: {e}")
        
        # ============================================================================
        # FOLDER OPERATIONS
        # ============================================================================
        
        print("\n\n2. Folder Operations")
        print("-" * 50)
        
        # Create a folder
        print("Creating a folder...")
        folder_request = FoldersFolderCreateRequest(
            name="Contracts"
        )
        folder = client.create_folder(folder_request)
        print(f"Folder created with ID: {folder.id}")
        
        # Get folder details
        print("\nGetting folder details...")
        folder_details = client.get_folder(folder.id)
        print(f"Folder name: {folder_details.name}")
        
        # List folders
        print("\nListing folders...")
        try:
            folders = client.list_folders(limit=10)
            if hasattr(folders, 'items') and folders.items is not None:
                print(f"Found {len(folders.items)} folders")
                if folders.items:
                    print(f"First folder: {folders.items[0].name if hasattr(folders.items[0], 'name') else 'Unknown'}")
            else:
                print("No folders found or items property is None")
        except Exception as e:
            print(f"Error listing folders: {e}")
        
        # Move document to folder
        print("\nMoving document to folder...")
        client.move_document_to_folder(document.document_id, folder.id)
        print("Document moved to folder")
        
        # Move documents in batch
        print("\nMoving documents in batch...")
        batch_result = client.move_documents_batch_to_folder([document.document_id], folder.id)
        print(f"Batch operation completed: {len(batch_result)} items processed")
        
        # ============================================================================
        # FLOW OPERATIONS
        # ============================================================================
        
        print("\n\n3. Flow Operations")
        print("-" * 50)
        
        # Create a signature flow
        print("Creating a signature flow...")
        signers = [
            {
                'name': 'Jack Bauer',
                'email': 'jack.bauer@mailinator.com',
                'identifier': '75502846369'
            },
            {
                'name': 'James Bond',
                'email': 'james.bond@mailinator.com',
                'identifier': '95588148061'
            }
        ]
        
        flow = client.create_signature_flow(
            document_id=document.document_id,
            signers=signers,
            title="Multi-party Contract",
            description="Contract requiring multiple signatures",
            expires_at="2024-12-31T23:59:59Z"
        )
        print(f"Flow created with ID: {flow.id}")
        
        # Get flow details
        print("\nGetting flow details...")
        flow_details = client.get_signature_flow(flow.id)
        print(f"Flow title: {flow_details.title}")
        print(f"Flow status: {flow_details.status}")
        
        # List flows
        print("\nListing flows...")
        flows = client.list_signature_flows(limit=5)
        print(f"Found {len(flows)} flows")
        
        # Update flow
        print("\nUpdating flow...")
        update_request = DocumentsDocumentFlowEditRequest(
            title="Updated Multi-party Contract",
            description="Updated description"
        )
        updated_flow = client.update_signature_flow(flow.id, update_request)
        print(f"Flow updated: {updated_flow.title}")

        # ============================================================================
        # NOTIFICATION OPERATIONS
        # ============================================================================
        
        print("\n\n5. Notification Operations")
        print("-" * 50)
        
        # Send reminder
        print("Sending reminder...")
        # Note: You need a valid flow_action_id for this to work
        client.send_reminder("", "Please sign the document")
        print("Reminder sent (commented out - needs valid flow_action_id)")
        
        # Notify pending users
        print("\nNotifying pending users...")
        emails = ["signer@example.com", "approver@example.com"]
        client.notify_pending_users(emails)
        print("Notifications sent to pending users")
        
        # ============================================================================
        # ORGANIZATION OPERATIONS
        # ============================================================================
        
        print("\n\n6. Organization Operations")
        print("-" * 50)
        
        # List organization users
        print("Listing organization users...")
        try:
            users = client.list_organization_users(limit=10)
            if hasattr(users, 'items') and users.items is not None:
                print(f"Found {len(users.items)} users")
                if users.items:
                    print(f"First user: {users.items[0].name if hasattr(users.items[0], 'name') else 'Unknown'}")
            else:
                print("No users found or items property is None")
        except Exception as e:
            print(f"Error listing organization users: {e}")
        
        # Add organization user
        print("\nAdding organization user...")
        user_request = OrganizationsOrganizationUserPostRequest(
            name="New User",
            email="newuser@example.com"
        )
        new_user = client.add_organization_user(user_request)
        print(f"User added with ID: {new_user.id}")
        
        # Remove organization user
        print("\nRemoving organization user...")
        client.remove_organization_user(new_user.id)
        print("User removed")
        
        # ============================================================================
        # MARKS SESSIONS OPERATIONS
        # ============================================================================
        
        print("\n\n7. Marks Sessions Operations")
        print("-" * 50)
        
        # Create marks session
        print("Creating marks session...")
        session_request = DocumentMarkMarksSessionCreateRequest(
            name="Contract Positioning Session",
            description="Session for positioning signature marks"
        )
        session = client.create_marks_session(session_request)
        print(f"Session created with ID: {session.id}")
        
        # Get marks session
        print("\nGetting marks session...")
        session_details = client.get_marks_session(session.id)
        print(f"Session name: {session_details.name}")
        print(f"Session status: {session_details.status}")
        
        # ============================================================================
        # DOCUMENT VERSION OPERATIONS
        # ============================================================================
        
        print("\n\n8. Document Version Operations")
        print("-" * 50)
        
        # Create document version
        print("Creating document version...")
        version_request = DocumentsDocumentAddVersionRequest(
            file_id=uploaded_file.id,
            title="Updated Contract Version"
        )
        version = client.create_document_version(document.id, version_request)
        print(f"Version created with ID: {version.id}")
        
        # Create envelope version
        print("\nCreating envelope version...")
        envelope_request = DocumentsEnvelopeAddVersionRequest(
            file_id=uploaded_file.id,
            title="Envelope Version"
        )
        envelope = client.create_document_envelope_version(document.id, envelope_request)
        print(f"Envelope version created with ID: {envelope.id}")
        
        # ============================================================================
        # DOCUMENT MANAGEMENT OPERATIONS
        # ============================================================================
        
        print("\n\n9. Document Management Operations")
        print("-" * 50)
        
        # Update notified emails
        print("Updating notified emails...")
        emails = ["admin@example.com", "manager@example.com"]
        client.update_document_notified_emails(document.id, emails)
        print("Notified emails updated")
        
        # Download signed document
        print("\nDownloading signed document...")
        client.download_signed_document(document.id, "downloaded_signed_document.pdf")
        print("Document downloaded")
        
        # Cancel document
        print("\nCanceling document...")
        cancellation_request = DocumentsCancelDocumentRequest(
            reason="Document no longer needed"
        )
        # client.cancel_document(document.id, cancellation_request)
        print("Document canceled (commented out to avoid actual cancellation)")
        
        # Refuse document
        print("\nRefusing document...")
        refusal_request = RefusalRefusalRequest(
            reason="Terms not acceptable"
        )
        # client.refuse_document(document.id, refusal_request)
        print("Document refused (commented out to avoid actual refusal)")
        
        # Delete folder
        print("\nDeleting folder...")
        delete_request = FoldersFolderDeleteRequest(
            delete_documents=True
        )
        # client.delete_folder(folder.id, delete_request)
        print("Folder deleted (commented out to avoid actual deletion)")
        
        # Delete flow
        print("\nDeleting flow...")
        # client.delete_signature_flow(flow.id)
        print("Flow deleted (commented out to avoid actual deletion)")
        
        # Delete document
        print("\nDeleting document...")
        # client.delete_document(document.id)
        print("Document deleted (commented out to avoid actual deletion)")
        
        print("\n=== All examples completed successfully! ===")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        client.close()


def example_with_context_manager():
    """Example using the context manager for automatic cleanup."""
    
    print("\n=== Context Manager Example ===")
    
    with create_signer_client(API_KEY, BASE_URL) as client:
        # Your operations here
        try:
            documents = client.list_documents(limit=1)
            if hasattr(documents, 'items') and documents.items is not None:
                print(f"Found {len(documents.items)} documents")
            else:
                print("No documents found")
        except Exception as e:
            print(f"Error listing documents: {e}")
    
    print("Client automatically closed")


def simple_status_example():
    """Simple example that just returns document status."""
    # You would need to replace this with an actual document ID
    document_id = "your-document-id-here"
    
    try:
        status = get_document_status_simple(document_id)
        print(f"Document {document_id} status: {status}")
        return status
    except Exception as e:
        print(f"Error getting status: {e}")
        return None


if __name__ == "__main__":
    # Check if API key is set
    if API_KEY == "":
        print("Please set your API key in the script before running.")
        print("You can get your API key from the Lacuna Signer dashboard.")
    else:
        status = main()
        print(f"Returned status: {status}")
        # example_with_context_manager() 