#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Publish Signer Python Client to PyPI

.DESCRIPTION
    This script builds and publishes the signer-python-client package to PyPI.
    It includes options for TestPyPI (testing) and production PyPI.
    All operations are performed inside the dist directory.

.PARAMETER Environment
    The target environment: "test" for TestPyPI or "prod" for production PyPI.
    Default is "test".

.PARAMETER SkipBuild
    Skip the build step if packages already exist.

.PARAMETER SkipCheck
    Skip the package validation check.

.EXAMPLE
    .\publish.ps1 -Environment test
    .\publish.ps1 -Environment prod
    .\publish.ps1 -Environment test -SkipBuild
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("test", "prod")]
    [string]$Environment = "test",
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipBuild,
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipCheck
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Colors for output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Blue"

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

function Test-PythonPackage {
    param([string]$PackagePath)
    try {
        $result = twine check $PackagePath 2>&1
        if ($LASTEXITCODE -eq 0) {
            return $true
        }
        return $false
    }
    catch {
        return $false
    }
}

# Script header
Write-ColorOutput "==========================================" $Blue
Write-ColorOutput "    Signer Python Client Publisher" $Blue
Write-ColorOutput "==========================================" $Blue
Write-ColorOutput ""

# Store original directory
$originalDir = Get-Location

# Change to dist directory
Write-ColorOutput "Changing to dist directory..." $Yellow
Set-Location "dist"

# Check if we're in the right directory (should have setup.py)
if (-not (Test-Path "setup.py")) {
    Write-ColorOutput "Error: setup.py not found in dist directory. Please ensure the dist directory contains the package files." $Red
    Set-Location $originalDir
    exit 1
}

# Check Python installation
Write-ColorOutput "Checking Python installation..." $Yellow
if (-not (Test-Command "python")) {
    Write-ColorOutput "Error: Python is not installed or not in PATH." $Red
    Set-Location $originalDir
    exit 1
}

$pythonVersion = python --version 2>&1
Write-ColorOutput "Found: $pythonVersion" $Green

# Check required tools
Write-ColorOutput "Checking required tools..." $Yellow

$requiredTools = @("pip", "build", "twine")
$missingTools = @()

foreach ($tool in $requiredTools) {
    if (-not (Test-Command $tool)) {
        $missingTools += $tool
    }
}

if ($missingTools.Count -gt 0) {
    Write-ColorOutput "Installing missing tools: $($missingTools -join ', ')" $Yellow
    python -m pip install --upgrade $missingTools
}

Write-ColorOutput "All required tools are available." $Green

# Clean previous builds
if (-not $SkipBuild) {
    Write-ColorOutput "Cleaning previous build artifacts..." $Yellow
    Remove-Item -Recurse -Force build, dist, *.egg-info -ErrorAction SilentlyContinue
    Write-ColorOutput "Cleanup completed." $Green
}

# Build the package
if (-not $SkipBuild) {
    Write-ColorOutput "Building package..." $Yellow
    python -m build
    
    if ($LASTEXITCODE -ne 0) {
        Write-ColorOutput "Error: Build failed!" $Red
        Set-Location $originalDir
        exit 1
    }
    Write-ColorOutput "Build completed successfully." $Green
}

# Check if build artifacts exist
$wheelFile = Get-ChildItem -Path "dist" -Filter "*.whl" -ErrorAction SilentlyContinue
$tarFile = Get-ChildItem -Path "dist" -Filter "*.tar.gz" -ErrorAction SilentlyContinue

if (-not $wheelFile -or -not $tarFile) {
    Write-ColorOutput "Error: Build artifacts not found. Please run build first." $Red
    Set-Location $originalDir
    exit 1
}

Write-ColorOutput "Found build artifacts:" $Green
Write-ColorOutput "  Wheel: $($wheelFile.Name)" $Green
Write-ColorOutput "  Source: $($tarFile.Name)" $Green

# Validate packages
if (-not $SkipCheck) {
    Write-ColorOutput "Validating packages..." $Yellow
    $wheelValid = Test-PythonPackage $wheelFile.FullName
    $tarValid = Test-PythonPackage $tarFile.FullName
    
    if (-not $wheelValid -or -not $tarValid) {
        Write-ColorOutput "Error: Package validation failed!" $Red
        Write-ColorOutput "Wheel valid: $wheelValid" $Red
        Write-ColorOutput "Tar valid: $tarValid" $Red
        Set-Location $originalDir
        exit 1
    }
    Write-ColorOutput "Package validation passed." $Green
}

# Determine target repository
$repository = if ($Environment -eq "test") { "testpypi" } else { "pypi" }
$repositoryUrl = if ($Environment -eq "test") { "https://test.pypi.org/legacy/" } else { "https://upload.pypi.org/legacy/" }

Write-ColorOutput ""
Write-ColorOutput "==========================================" $Blue
Write-ColorOutput "Ready to publish to: $($Environment.ToUpper())" $Blue
Write-ColorOutput "Repository: $repository" $Blue
Write-ColorOutput "URL: $repositoryUrl" $Blue
Write-ColorOutput "==========================================" $Blue
Write-ColorOutput ""

# Confirmation prompt
$confirmation = Read-Host "Do you want to proceed with publishing? (y/N)"
if ($confirmation -ne "y" -and $confirmation -ne "Y") {
    Write-ColorOutput "Publishing cancelled." $Yellow
    Set-Location $originalDir
    exit 0
}

# Publish to PyPI
Write-ColorOutput "Publishing to $($Environment.ToUpper())..." $Yellow

try {
    $uploadArgs = @(
        "upload",
        "--repository", $repository,
        $wheelFile.FullName,
        $tarFile.FullName
    )
    
    twine @uploadArgs
    
    if ($LASTEXITCODE -eq 0) {
        Write-ColorOutput ""
        Write-ColorOutput "==========================================" $Green
        Write-ColorOutput "SUCCESS: Package published successfully!" $Green
        Write-ColorOutput "==========================================" $Green
        
        if ($Environment -eq "test") {
            Write-ColorOutput ""
            Write-ColorOutput "TestPyPI URL: https://test.pypi.org/project/signer-python-client/" $Blue
            Write-ColorOutput "Install command: pip install -i https://test.pypi.org/simple/ signer-python-client" $Blue
        } else {
            Write-ColorOutput ""
            Write-ColorOutput "PyPI URL: https://pypi.org/project/signer-python-client/" $Blue
            Write-ColorOutput "Install command: pip install signer-python-client" $Blue
        }
    } else {
        Write-ColorOutput "Error: Publishing failed!" $Red
        Set-Location $originalDir
        exit 1
    }
}
catch {
    Write-ColorOutput "Error during publishing: $($_.Exception.Message)" $Red
    Set-Location $originalDir
    exit 1
}

# Return to original directory
Set-Location $originalDir

Write-ColorOutput ""
Write-ColorOutput "Publishing completed!" $Green 