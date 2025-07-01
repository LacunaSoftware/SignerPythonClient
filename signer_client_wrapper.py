"""
Lacuna Signer Python Client Wrapper

A user-friendly wrapper for the Lacuna Signer API that provides high-level operations
for digital signatures, document management, and workflow automation.

Based on the Lacuna Signer documentation: https://docs.lacunasoftware.com/pt-br/articles/signer/index.html
"""

import os
import base64
from typing import List, Dict, Optional, Union, BinaryIO
from pathlib import Path

# Import the generated client
from dist.signer_client import (
    Configuration, ApiClient,
    DocumentsApi, FlowsApi, FoldersApi, MarksSessionsApi, 
    NotificationsApi, OrganizationsApi, UploadApi
)
from dist.signer_client.models import (
    DocumentsCreateDocumentRequest, DocumentsCreateDocumentResult,
    DocumentsDocumentModel, DocumentsDocumentListModel,
    DocumentFlowsDocumentFlowCreateRequest, DocumentFlowsDocumentFlowModel,
    FoldersFolderCreateRequest, FoldersFolderInfoModel,
    UploadsUploadBytesRequest, UploadsUploadBytesModel,
    FlowActionsFlowActionCreateModel, FlowActionsFlowActionModel,
    UsersParticipantUserModel, DocumentsDocumentFileModel,
    DocumentStatus, DocumentTypes, FolderType, FlowActionType,
    SignatureTypes, AuthenticationTypes
)


class SignerClient:
    """
    A comprehensive client for the Lacuna Signer API that provides high-level operations
    for digital signatures and document management.
    
    The Lacuna Signer is an intelligent signature manager that allows you to collect
    different types of signatures with a fast, intuitive, and customizable system.
    
    Features:
    - Digital and electronic signatures with legal validity
    - Individual instances for each client with separate databases and storage
    - Support for various document types (contracts, proposals, medical reports, etc.)
    """
    
    def __init__(self, api_key: str, base_url: str = "https://signer-lac.azurewebsites.net"):
        """
        Initialize the Signer client.
        
        Args:
            api_key: Your API key in the format 'your-app|xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            base_url: The base URL for the Signer API (defaults to production)
        """
        self.config = Configuration()
        self.config.host = base_url
        self.config.api_key['X-Api-Key'] = api_key
        
        self.api_client = ApiClient(self.config)
        
        # Initialize all API clients
        self.documents = DocumentsApi(self.api_client)
        self.flows = FlowsApi(self.api_client)
        self.folders = FoldersApi(self.api_client)
        self.marks_sessions = MarksSessionsApi(self.api_client)
        self.notifications = NotificationsApi(self.api_client)
        self.organizations = OrganizationsApi(self.api_client)
        self.upload = UploadApi(self.api_client)
    
    # ============================================================================
    # DOCUMENT MANAGEMENT
    # ============================================================================
    
    def create_document(self, 
                       file_path: Union[str, Path, BinaryIO],
                       title: str,
                       description: Optional[str] = None,
                       document_type: Optional[DocumentTypes] = None,
                       folder_id: Optional[str] = None,
                       tags: Optional[List[str]] = None) -> DocumentsCreateDocumentResult:
        """
        Create a new document for signing.
        
        Args:
            file_path: Path to the document file or file-like object
            title: Document title
            description: Optional document description
            document_type: Type of document (contract, proposal, etc.)
            folder_id: Optional folder ID to organize the document
            tags: Optional list of tags for categorization
            
        Returns:
            Document creation result with document ID and metadata
        """
        # Upload the file first
        upload_result = self.upload_file(file_path)
        
        # Create document request
        request = DocumentsCreateDocumentRequest(
            title=title,
            description=description,
            document_type=document_type,
            folder_id=folder_id,
            tags=tags,
            files=[DocumentsDocumentFileModel(
                id=upload_result.id,
                name=upload_result.name,
                content_type=upload_result.content_type
            )]
        )
        
        return self.documents.api_documents_post(body=request)
    
    def get_document(self, document_id: str) -> DocumentsDocumentModel:
        """
        Retrieve a specific document by ID.
        
        Args:
            document_id: The document ID
            
        Returns:
            Document model with all details
        """
        return self.documents.api_documents_id_get(document_id)
    
    def list_documents(self, 
                      status: Optional[DocumentStatus] = None,
                      folder_id: Optional[str] = None,
                      document_type: Optional[DocumentTypes] = None,
                      limit: int = 20,
                      offset: int = 0) -> DocumentsDocumentListModel:
        """
        List documents with optional filtering.
        
        Args:
            status: Filter by document status (pending, concluded, etc.)
            folder_id: Filter by folder ID
            document_type: Filter by document type
            limit: Number of documents to return
            offset: Pagination offset
            
        Returns:
            Paginated list of documents
        """
        return self.documents.api_documents_get(
            status=status,
            folder_id=folder_id,
            document_type=document_type,
            limit=limit,
            offset=offset
        )
    
    def download_document(self, document_id: str, output_path: Optional[Union[str, Path]] = None) -> bytes:
        """
        Download a document's content.
        
        Args:
            document_id: The document ID
            output_path: Optional path to save the file
            
        Returns:
            Document content as bytes
        """
        content = self.documents.api_documents_id_content_get(document_id)
        
        if output_path:
            with open(output_path, 'wb') as f:
                f.write(content)
        
        return content
    
    def delete_document(self, document_id: str) -> None:
        """
        Delete a document.
        
        Args:
            document_id: The document ID to delete
        """
        self.documents.api_documents_id_delete(document_id)
    
    # ============================================================================
    # SIGNATURE FLOW MANAGEMENT
    # ============================================================================
    
    def create_signature_flow(self, 
                            document_id: str,
                            signers: List[Dict],
                            title: Optional[str] = None,
                            description: Optional[str] = None,
                            expires_at: Optional[str] = None) -> DocumentFlowsDocumentFlowModel:
        """
        Create a signature flow for a document.
        
        Args:
            document_id: The document to be signed
            signers: List of signer dictionaries with keys:
                     - name: Signer's name
                     - email: Signer's email
                     - cpf: Signer's CPF (Brazilian ID)
                     - signature_type: Type of signature (digital, electronic, etc.)
            title: Optional flow title
            description: Optional flow description
            expires_at: Optional expiration date (ISO format)
            
        Returns:
            Created flow model
        """
        # Create flow actions for each signer
        flow_actions = []
        for i, signer in enumerate(signers):
            action = FlowActionsFlowActionCreateModel(
                type=FlowActionType.SIGNER,
                order=i + 1,
                user=UsersParticipantUserModel(
                    name=signer['name'],
                    email=signer['email'],
                    cpf=signer.get('cpf')
                ),
                signature_type=signer.get('signature_type', SignatureTypes.DIGITAL),
                authentication_type=signer.get('authentication_type', AuthenticationTypes.EMAIL)
            )
            flow_actions.append(action)
        
        # Create flow request
        flow_request = DocumentFlowsDocumentFlowCreateRequest(
            title=title,
            description=description,
            expires_at=expires_at,
            flow_actions=flow_actions
        )
        
        return self.flows.api_document_flows_post(body=flow_request)
    
    def get_signature_flow(self, flow_id: str) -> DocumentFlowsDocumentFlowModel:
        """
        Get signature flow details.
        
        Args:
            flow_id: The flow ID
            
        Returns:
            Flow model with all details
        """
        return self.flows.api_document_flows_id_get(flow_id)
    
    def list_signature_flows(self, limit: int = 20, offset: int = 0) -> List[DocumentFlowsDocumentFlowModel]:
        """
        List signature flows.
        
        Args:
            limit: Number of flows to return
            offset: Pagination offset
            
        Returns:
            List of flow models
        """
        response = self.flows.api_document_flows_get(limit=limit, offset=offset)
        return response.items if hasattr(response, 'items') else response
    
    def cancel_signature_flow(self, flow_id: str, reason: Optional[str] = None) -> None:
        """
        Cancel a signature flow.
        
        Args:
            flow_id: The flow ID to cancel
            reason: Optional cancellation reason
        """
        self.flows.api_document_flows_id_delete(flow_id)
    
    # ============================================================================
    # FOLDER MANAGEMENT
    # ============================================================================
    
    def create_folder(self, 
                     name: str,
                     description: Optional[str] = None,
                     parent_folder_id: Optional[str] = None) -> FoldersFolderInfoModel:
        """
        Create a new folder for organizing documents.
        
        Args:
            name: Folder name
            description: Optional folder description
            parent_folder_id: Optional parent folder ID for nested folders
            
        Returns:
            Created folder model
        """
        request = FoldersFolderCreateRequest(
            name=name,
            description=description,
            parent_folder_id=parent_folder_id
        )
        
        return self.folders.api_folders_post(body=request)
    
    def get_folder(self, folder_id: str) -> FoldersFolderInfoModel:
        """
        Get folder details.
        
        Args:
            folder_id: The folder ID
            
        Returns:
            Folder model with details
        """
        return self.folders.api_folders_id_get(folder_id)
    
    def list_folders(self, limit: int = 20, offset: int = 0) -> List[FoldersFolderInfoModel]:
        """
        List folders.
        
        Args:
            limit: Number of folders to return
            offset: Pagination offset
            
        Returns:
            List of folder models
        """
        response = self.folders.api_folders_get(limit=limit, offset=offset)
        return response.items if hasattr(response, 'items') else response
    
    def delete_folder(self, folder_id: str) -> None:
        """
        Delete a folder.
        
        Args:
            folder_id: The folder ID to delete
        """
        self.folders.api_folders_id_delete_post(folder_id)
    
    # ============================================================================
    # FILE UPLOAD
    # ============================================================================
    
    def upload_file(self, file_path: Union[str, Path, BinaryIO]) -> UploadsUploadBytesModel:
        """
        Upload a file to the Signer platform.
        
        Args:
            file_path: Path to the file or file-like object
            
        Returns:
            Upload result with file ID and metadata
        """
        if isinstance(file_path, (str, Path)):
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            with open(file_path, 'rb') as f:
                content = f.read()
            filename = file_path.name
        else:
            # Assume it's a file-like object
            content = file_path.read()
            filename = getattr(file_path, 'name', 'uploaded_file')
        
        # Encode content as base64
        content_b64 = base64.b64encode(content).decode('utf-8')
        
        request = UploadsUploadBytesRequest(
            content=content_b64,
            name=filename
        )
        
        return self.upload.api_uploads_bytes_post(body=request)
    
    # ============================================================================
    # NOTIFICATIONS
    # ============================================================================
    
    def send_reminder(self, flow_action_id: str, message: Optional[str] = None) -> None:
        """
        Send a reminder to a signer.
        
        Args:
            flow_action_id: The flow action ID (signer's pending action)
            message: Optional custom reminder message
        """
        request = {
            'flow_action_id': flow_action_id
        }
        if message:
            request['message'] = message
        
        self.notifications.api_notifications_flow_action_reminder_post(body=request)
    
    def notify_pending_users(self, email_list: List[str]) -> None:
        """
        Send notifications to users with pending actions.
        
        Args:
            email_list: List of email addresses to notify
        """
        request = {
            'email_list': email_list
        }
        
        self.notifications.api_users_notify_pending_post(body=request)
    
    # ============================================================================
    # ORGANIZATION MANAGEMENT
    # ============================================================================
    
    def get_organization_info(self):
        """
        Get current organization information.
        
        Returns:
            Organization information model
        """
        return self.organizations.api_organizations_get()
    
    def list_organization_users(self, limit: int = 20, offset: int = 0):
        """
        List users in the organization.
        
        Args:
            limit: Number of users to return
            offset: Pagination offset
            
        Returns:
            List of organization user models
        """
        response = self.organizations.api_organizations_users_get(limit=limit, offset=offset)
        return response.items if hasattr(response, 'items') else response
    
    # ============================================================================
    # HIGH-LEVEL OPERATIONS
    # ============================================================================
    
    def sign_document_simple(self, 
                           file_path: Union[str, Path, BinaryIO],
                           title: str,
                           signers: List[Dict],
                           folder_name: Optional[str] = None) -> Dict:
        """
        High-level method to create a document and signature flow in one operation.
        
        Args:
            file_path: Path to the document file
            title: Document title
            signers: List of signer dictionaries
            folder_name: Optional folder name to create and organize the document
            
        Returns:
            Dictionary with document and flow information
        """
        # Create folder if specified
        folder_id = None
        if folder_name:
            folder = self.create_folder(folder_name)
            folder_id = folder.id
        
        # Create document
        document = self.create_document(
            file_path=file_path,
            title=title,
            folder_id=folder_id
        )
        
        # Create signature flow
        flow = self.create_signature_flow(
            document_id=document.id,
            signers=signers
        )
        
        return {
            'document': document,
            'flow': flow,
            'folder_id': folder_id
        }
    
    def get_document_status(self, document_id: str) -> Dict:
        """
        Get comprehensive document status including signatures.
        
        Args:
            document_id: The document ID
            
        Returns:
            Dictionary with document status and signature information
        """
        document = self.get_document(document_id)
        signatures_info = self.documents.api_documents_id_signatures_details_get(document_id)
        
        return {
            'document': document,
            'signatures': signatures_info,
            'status': document.status,
            'is_concluded': document.status == DocumentStatus.CONCLUDED
        }
    
    def validate_signatures(self, document_content: bytes) -> Dict:
        """
        Validate signatures in a document.
        
        Args:
            document_content: Document content as bytes
            
        Returns:
            Validation results
        """
        content_b64 = base64.b64encode(document_content).decode('utf-8')
        request = {
            'content': content_b64
        }
        
        return self.documents.api_documents_validate_signatures_post(body=request)
    
    def get_action_url(self, document_id: str, flow_action_id: str) -> str:
        """
        Get the URL for a signer to access and sign a document.
        
        Args:
            document_id: The document ID
            flow_action_id: The flow action ID (signer's action)
            
        Returns:
            URL for the signer to access
        """
        request = {
            'flow_action_id': flow_action_id
        }
        
        response = self.documents.api_documents_id_action_url_post(document_id, body=request)
        return response.url
    
    # ============================================================================
    # UTILITY METHODS
    # ============================================================================
    
    def close(self):
        """Close the API client and clean up resources."""
        if hasattr(self.api_client, 'close'):
            self.api_client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# Convenience function for quick setup
def create_signer_client(api_key: str, base_url: str = "https://signer-lac.azurewebsites.net") -> SignerClient:
    """
    Create a SignerClient instance with the given API key.
    
    Args:
        api_key: Your API key
        base_url: Optional base URL (defaults to production)
        
    Returns:
        Configured SignerClient instance
    """
    return SignerClient(api_key, base_url)


# Example usage
if __name__ == "__main__":
    # Example of how to use the SignerClient
    api_key = "your-app|xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    
    with create_signer_client(api_key) as client:
        # Create a document and signature flow
        signers = [
            {
                "name": "João Silva",
                "email": "joao.silva@example.com",
                "cpf": "12345678901",
                "signature_type": "DIGITAL"
            },
            {
                "name": "Maria Santos",
                "email": "maria.santos@example.com",
                "cpf": "98765432100",
                "signature_type": "ELECTRONIC"
            }
        ]
        
        # Create document and flow
        result = client.sign_document_simple(
            file_path="contract.pdf",
            title="Employment Contract",
            signers=signers,
            folder_name="Contracts"
        )
        
        print(f"Document created: {result['document'].id}")
        print(f"Flow created: {result['flow'].id}")
        
        # Get document status
        status = client.get_document_status(result['document'].id)
        print(f"Document status: {status['status']}")
        
        # List documents
        documents = client.list_documents(limit=10)
        print(f"Found {len(documents.items)} documents") 