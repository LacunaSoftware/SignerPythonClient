# Generate the library using swagger-codegen
# If the file is not present, download it
if (-not (Test-Path -Path swagger-codegen-cli.jar)) {
    wget https://repo1.maven.org/maven2/io/swagger/codegen/v3/swagger-codegen-cli/3.0.68/swagger-codegen-cli-3.0.68.jar -O swagger-codegen-cli.jar
}

# Generate the library
java -jar swagger-codegen-cli.jar generate -i https://signer-lac.azurewebsites.net/swagger/api/swagger.json -l python -o ./dist -c swagger-codegen-config-simple.json   

# Manual files section

# Copy the manually_generated_files/client.py file to dist/signer_client/client.py
Copy-Item -Path "manually_generated_files/client.py" -Destination "dist/signer_client/client.py" -Force

# Copy the manually_generated_files/documents_create_document_request.py file to dist/signer_client/models/documents_create_document_request.py
Copy-Item -Path "manually_generated_files/documents_create_document_request.py" -Destination "dist/signer_client/models/documents_create_document_request.py" -Force

# End of manual files section

# Add the import statement to dist/signer_client/__init__.py
if (Test-Path -Path "dist/signer_client/__init__.py") {
    $content = Get-Content "dist/signer_client/__init__.py" -Raw
    if ($content -notmatch "from signer_client.client import SignerClient") {
        Add-Content "dist/signer_client/__init__.py" "from signer_client.client import SignerClient"
    }
} else {
    # Throw an error
    throw "dist/signer_client/__init__.py not found"
}

# Show message that the library was generated successfully
Write-Host "Library generated successfully! The content is in the dist folder."

# Write next steps
Write-Host "Next steps:"
Write-Host "1. Run the following command to install the library in your environment:"
Write-Host "   cd dist"
Write-Host "   python -m pip install -r requirements.txt ; python setup.py build; python .\setup.py install"
