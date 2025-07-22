# Setup script for AKS AI Agent
# Run this script to set up the complete environment

Write-Host "🚀 Setting up AKS AI Agent Environment" -ForegroundColor Green

# 1. Check prerequisites
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow

# Check if Azure CLI is installed
try {
    az version | Out-Null
    Write-Host "✅ Azure CLI is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure CLI is not installed. Please install it first." -ForegroundColor Red
    exit 1
}

# Check if kubectl is installed
try {
    kubectl version --client | Out-Null
    Write-Host "✅ kubectl is installed" -ForegroundColor Green
} catch {
    Write-Host "⚠️ kubectl not found. Installing via Azure CLI..." -ForegroundColor Yellow
    az aks install-cli
}

# Check if Terraform is installed
try {
    terraform version | Out-Null
    Write-Host "✅ Terraform is installed" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Terraform not found. Installing via winget..." -ForegroundColor Yellow
    winget install Hashicorp.Terraform
}

# Check if Node.js is installed
try {
    node --version | Out-Null
    Write-Host "✅ Node.js is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js is not installed. Please install it first." -ForegroundColor Red
    exit 1
}

# 2. Create Python virtual environment
Write-Host "🐍 Creating Python virtual environment..." -ForegroundColor Yellow
python -m venv venv
Write-Host "✅ Virtual environment created" -ForegroundColor Green

# 3. Activate virtual environment and install packages
Write-Host "📦 Installing Python packages..." -ForegroundColor Yellow
./venv/Scripts/Activate.ps1
pip install -r requirements.txt
Write-Host "✅ Python packages installed" -ForegroundColor Green

# 4. Install MCP Kubernetes server
Write-Host "🔧 Installing MCP Kubernetes server..." -ForegroundColor Yellow
npm install -g mcp-server-kubernetes
Write-Host "✅ MCP Kubernetes server installed" -ForegroundColor Green

# 5. Initialize Terraform
Write-Host "🏗️ Initializing Terraform..." -ForegroundColor Yellow
Set-Location terraform
terraform init
Write-Host "✅ Terraform initialized" -ForegroundColor Green
Set-Location ..

# 6. Create .env file
Write-Host "⚙️ Creating environment file..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "✅ .env file created from template" -ForegroundColor Green
    Write-Host "📝 Please edit .env file with your Azure OpenAI credentials" -ForegroundColor Cyan
} else {
    Write-Host "⚠️ .env file already exists" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file with your Azure OpenAI credentials" -ForegroundColor White
Write-Host "2. Deploy AKS cluster: cd terraform && terraform plan && terraform apply" -ForegroundColor White
Write-Host "3. Configure kubectl: az aks get-credentials --resource-group <rg-name> --name <cluster-name>" -ForegroundColor White
Write-Host "4. Run the agent: ./venv/Scripts/Activate.ps1 && chainlit run app_ui.py -w" -ForegroundColor White
