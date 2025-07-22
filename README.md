# AKS AI Agent - Kubernetes Discovery and Assessment

An intelligent AI agent that discovers and assesses Kubernetes clusters using Azure OpenAI and Model Context Protocol (MCP).

## 🏗️ Architecture

- **Local**: Semantic Kernel + Chainlit (Python virtual environment)
- **Cloud**: AKS cluster + Azure OpenAI (Azure AI Foundry)

## 🚀 Quick Start

### 1. Prerequisites
- Azure CLI (logged in)
- Python 3.8+
- Node.js 16+
- PowerShell

### 2. Automated Setup
```powershell
# Run the setup script
./setup.ps1
```

### 3. Configure Azure OpenAI
1. Deploy Azure OpenAI in Azure AI Foundry
2. Create a GPT-4 deployment
3. Copy endpoint and API key to `.env` file

### 4. Deploy AKS Cluster
```powershell
cd terraform
terraform validate
terraform plan
terraform apply
```

### 5. Configure kubectl
```powershell
# Use the output from terraform apply
az aks get-credentials --resource-group rg-aks-ai-agent-dev --name aks-ai-agent-cluster
```

### 6. Run the Agent
```powershell
./start.ps1
```

## 📁 Project Structure

```
├── terraform/          # AKS cluster infrastructure
│   ├── main.tf         # Main Terraform configuration
│   ├── variables.tf    # Variable definitions
│   └── terraform.tfvars # Variable values
├── app.py              # Main agent implementation
├── chainlit.py         # Chainlit web interface
├── utilities.py        # Helper functions
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
├── setup.ps1          # Automated setup script
└── start.ps1          # Quick start script
```

## ⚙️ Manual Setup (Alternative)

### Python Dependencies
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Node.js Dependencies
```bash
npm install -g mcp-server-kubernetes
```

### Azure Setup
1. Azure OpenAI resource with GPT-4 deployment
2. Update `.env` file with your endpoint and API key

### Kubernetes Setup
1. Deploy AKS cluster using Terraform
2. Configure kubectl access

## 🔧 Configuration

### Environment Variables (.env)
```bash
AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-01
```

### Terraform Variables (terraform.tfvars)
```hcl
resource_group_name = "rg-aks-ai-agent-dev"
location           = "East US"
cluster_name       = "aks-ai-agent-cluster"
acr_name          = "acraksiagent001"  # Must be globally unique
node_count        = 2
vm_size           = "Standard_D2s_v3"
```

## 🚀 Usage

The agent can help you:
- **Discover**: List namespaces, pods, services, deployments
- **Assess**: Analyze cluster health and resource usage
- **Report**: Generate detailed Markdown reports
- **Monitor**: Track cluster changes over time

### Example Queries
- "Show me all pods in the default namespace"
- "Generate a cluster summary report"
- "What deployments are running?"
- "Analyze node resource usage"

## 🔍 How It Works

1. **MCP Server**: Uses `mcp-server-kubernetes` to interact with Kubernetes API
2. **kubectl**: Leverages your local kubectl configuration for cluster access
3. **Semantic Kernel**: Orchestrates AI agent with Azure OpenAI
4. **Chainlit**: Provides user-friendly chat interface

## 🛠️ Troubleshooting

### Common Issues

1. **Cannot connect to cluster**
   ```powershell
   kubectl cluster-info
   az aks get-credentials --resource-group <rg> --name <cluster>
   ```

2. **MCP server not found**
   ```powershell
   npm install -g mcp-server-kubernetes
   ```

3. **Azure OpenAI errors**
   - Check endpoint and API key in `.env`
   - Verify deployment name matches your Azure OpenAI deployment

## 📚 Resources

- [Azure Kubernetes Service (AKS)](https://docs.microsoft.com/azure/aks/)
- [Azure OpenAI Service](https://docs.microsoft.com/azure/cognitive-services/openai/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Semantic Kernel](https://github.com/microsoft/semantic-kernel)
- [Chainlit](https://chainlit.io/)
