# Signer Python Client

A Python client library for the [Signer API](https://dropsigner.com/swagger/index.html)

## Installation

### From PyPI (when published)
```bash
pip install signer-client
```

### From source
```bash
git clone https://github.com/LacunaSoftware/SignerPythonClient.git
cd signer-python-client
pip install -e .
```

## Quick Start

### Using the High-Level SignerClient (Recommended)

The `SignerClient` provides a simplified interface for common operations:

```python
from signer_client import SignerClient, create_signer_client
from signer_client.models import (
    DocumentsCreateDocumentRequest, FileUploadModel, 
    UsersParticipantUserModel, FlowActionsFlowActionCreateModel,
    AuthenticationTypes, FlowActionType
)

# Initialize the client
client = SignerClient(
    api_key="your-app|xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    base_url="https://signer-demo.lacunasoftware.com"
)

# Create a document with signature flow
try:
    # Upload a file
    with open("document.pdf", "rb") as file:
        file_upload = client.upload_file("document.pdf")
    
    # Create signer
    signer = UsersParticipantUserModel(
        name="John Doe",
        email="john.doe@example.com",
        identifier="12345678901"  # Brazilian ID (optional)
    )
    
    # Create flow action
    flow_action = FlowActionsFlowActionCreateModel(
        type=FlowActionType.SIGNER,
        step=1,
        user=signer,
        authentication_type=AuthenticationTypes.EMAIL
    )
    
    # Create document request
    document_request = DocumentsCreateDocumentRequest(
        files=[file_upload],
        flow_actions=[flow_action],
        title="Contract Agreement"
    )
    
    # Create document with signature flow
    document = client.create_document(document_request)
    print(f"Document created: {document.id}")
    print(f"Status: {document.status}")
    
    # Get signing URL for the signer
    signing_url = client.get_signing_url(document.id, "john.doe@example.com")
    print(f"Signing URL: {signing_url}")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
```

### Using the Low-Level API Client

For more granular control, you can use the generated API client directly:

```python
from signer_client import ApiClient, Configuration
from signer_client.api import DocumentsApi

# Configure the API client
configuration = Configuration(
    host="https://signer-demo.lacunasoftware.com",
    api_key="your-app|xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
)

# Create API client
api_client = ApiClient(configuration)

# Use the Documents API
documents_api = DocumentsApi(api_client)

# Get a document by ID
try:
    document = documents_api.get_document("document-id-here")
    print(f"Document: {document.title}")
except Exception as e:
    print(f"Error: {e}")
```

## Authentication

The Signer API uses API key authentication. Set your API key in the configuration:

```python
# For SignerClient
client = SignerClient(
    api_key="your-app|xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
)

# For low-level API client
configuration = Configuration(
    api_key="your-app|xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
)
```

## Available APIs

The client includes the following API modules:

- **DocumentsApi**: Document management operations
- **FlowsApi**: Signature flow management
- **FoldersApi**: Folder management operations  
- **OrganizationsApi**: Organization management
- **FlowActionsApi**: Document flow and signature actions
- **UploadApi**: File upload operations
- **NotificationsApi**: Notification management
- **MarksSessionsApi**: Document mark positioning
- **WebhooksApi**: Webhook configuration and management

## Error Handling

The client provides comprehensive error handling with specific exception types:

```python
from signer_client.exceptions import ApiException

try:
    document = client.get_document("invalid-id")
except ApiException as e:
    if e.status == 404:
        print("Document not found")
    elif e.status == 401:
        print("Unauthorized - check your API key")
    else:
        print(f"API error: {e}")
```

## Webhooks

Configure webhooks to receive real-time notifications:

```python
from signer_client.api import WebhooksApi

webhooks_api = WebhooksApi(api_client)

# Register a webhook URL
webhook_config = {
    "url": "https://your-app.com/webhooks/signer",
    "events": ["DocumentSigned", "DocumentApproved", "DocumentRefused"]
}

webhook = webhooks_api.create_webhook(webhook_config)
```

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
```

### Type Checking
```bash
mypy .
```

## API Documentation

For detailed API documentation, visit the [Signer API Swagger UI](https://signer-lac.azurewebsites.net/swagger/index.html).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For support and questions:
- API Documentation: https://signer-lac.azurewebsites.net/swagger/index.html
- Issues: https://github.com/your-org/signer-python-client/issues 
