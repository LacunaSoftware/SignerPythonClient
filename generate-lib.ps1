# Generate the library using swagger-codegen
# If the file is not present, download it
if (-not (Test-Path -Path swagger-codegen-cli.jar)) {
    wget https://repo1.maven.org/maven2/io/swagger/codegen/v3/swagger-codegen-cli/3.0.68/swagger-codegen-cli-3.0.68.jar -O swagger-codegen-cli.jar
}

# Generate the library
java -jar swagger-codegen-cli.jar generate -i https://signer-lac.azurewebsites.net/swagger/api/swagger.json -l python -o ./dist -c swagger-codegen-config-simple.json   