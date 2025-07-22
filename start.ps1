# Quick start script to run the AKS AI Agent
# Make sure you've completed setup first!

Write-Host "🚀 Starting AKS AI Agent..." -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path "venv/Scripts/Activate.ps1")) {
    Write-Host "❌ Virtual environment not found. Run setup.ps1 first." -ForegroundColor Red
    exit 1
}

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found. Copy .env.example to .env and configure it." -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "🐍 Activating virtual environment..." -ForegroundColor Yellow
./venv/Scripts/Activate.ps1

# Check kubectl connection
Write-Host "🔍 Checking Kubernetes cluster connection..." -ForegroundColor Yellow
try {
    kubectl cluster-info | Out-Null
    Write-Host "✅ Connected to Kubernetes cluster" -ForegroundColor Green
} catch {
    Write-Host "❌ Cannot connect to Kubernetes cluster." -ForegroundColor Red
    Write-Host "Run: az aks get-credentials --resource-group <rg-name> --name <cluster-name>" -ForegroundColor Yellow
    exit 1
}

# Start the agent
Write-Host "🤖 Starting AKS AI Agent with Chainlit..." -ForegroundColor Green
chainlit run app_ui.py -w
