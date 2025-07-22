# AKS AI Agent - Complete Solution Overview

## 📋 **Project Summary**

This is a **Kubernetes Discovery AI Agent** that helps you explore and analyze your AKS (Azure Kubernetes Service) clusters using artificial intelligence. The solution runs locally on your machine and connects to your AKS cluster in Azure to provide intelligent insights and reports.

## 🎯 **What This Solution Does**

- **Discovers Kubernetes Resources**: Lists nodes, pods, services, namespaces
- **Generates Reports**: Creates detailed cluster analysis documents
- **AI-Powered Analysis**: Uses Azure OpenAI to provide intelligent insights
- **Web Interface**: Provides an easy-to-use chat interface via web browser
- **Local Execution**: Runs on your local machine, connects to remote AKS cluster

## 📁 **Complete File Structure & Usage**

### **🔧 Core Application Files (MUST HAVE)**

#### **`app.py` - Main Agent Logic** ⭐
- **Purpose**: Creates and configures the AI agent
- **What it does**: 
  - Connects to Azure OpenAI service
  - Sets up Kubernetes discovery capabilities
  - Creates the AI agent that can answer questions about your cluster
- **When used**: Called by `app_ui.py` when the web application starts
- **Dependencies**: Requires `.env` file with Azure OpenAI credentials

#### **`app_ui.py` - Web Interface** ⭐
- **Purpose**: Provides the web-based chat interface
- **What it does**:
  - Creates a web server on your local machine (port 8000)
  - Displays a chat interface in your browser
  - Sends your questions to the AI agent and displays responses
- **When used**: This is what you run to start the application
- **Command**: `chainlit run app_ui.py -w`

#### **`utilities.py` - Helper Functions** ⭐
- **Purpose**: Contains utility functions for file operations
- **What it does**:
  - Saves cluster reports to markdown files
  - Handles file writing operations
- **When used**: Called by the AI agent when generating reports

#### **`.env` - Configuration File** ⭐ **CRITICAL**
- **Purpose**: Stores your Azure OpenAI credentials and settings
- **What it contains**:
  - Azure OpenAI endpoint URL
  - API key for authentication
  - Model deployment name
  - API version
- **Security**: Contains sensitive information, never share this file

### **🏗️ Infrastructure Files (AZURE DEPLOYMENT)**

#### **`terraform/main.tf` - Infrastructure Definition**
- **Purpose**: Defines your Azure infrastructure using code
- **What it creates**:
  - AKS (Azure Kubernetes Service) cluster
  - Azure Container Registry (ACR)
  - Virtual networks and networking components
- **When used**: Run with `terraform apply` to create Azure resources

#### **`terraform/variables.tf` - Variable Definitions**
- **Purpose**: Defines configurable parameters for Terraform
- **What it contains**: Variable declarations (like cluster name, location, etc.)

#### **`terraform/terraform.tfvars` - Environment Values**
- **Purpose**: Contains actual values for the Terraform variables
- **What it contains**: Specific values like Azure region, cluster size, etc.

### **📦 Dependency & Configuration Files**

#### **`requirements.txt` - Python Dependencies**
- **Purpose**: Lists all Python packages needed by the application
- **Key packages**:
  - `semantic-kernel` - AI orchestration framework
  - `chainlit` - Web interface framework
  - `azure-identity` - Azure authentication
  - `python-dotenv` - Environment variable management
- **Usage**: `pip install -r requirements.txt`

#### **`chainlit.md` - Web Interface Configuration**
- **Purpose**: Auto-generated configuration for the web interface
- **Created by**: Chainlit framework automatically
- **Contains**: Welcome message and UI settings

### **📖 Documentation Files (REFERENCE)**

#### **`docs/ARCHITECTURE.md` - Technical Architecture**
- **Purpose**: Explains how all components work together
- **Content**: System diagrams, component relationships, technical details

#### **`DEPLOYMENT_STATUS.md` - Project Status**
- **Purpose**: Current status of deployment and testing
- **Content**: What's working, what's tested, next steps

#### **`README.md` - Project Overview**
- **Purpose**: Getting started guide and project introduction
- **Content**: Installation instructions, usage examples

### **🧪 Test Files (DEVELOPMENT & DEBUGGING)**

#### **`test/test_openai_connection.py`**
- **Purpose**: Tests connection to Azure OpenAI service
- **When to use**: To verify your Azure OpenAI setup is working

#### **`test/test_rest_api.py`**
- **Purpose**: Tests direct REST API connection to Azure OpenAI
- **When to use**: For troubleshooting connectivity issues

#### **`test/test_sk_explicit_settings.py`**
- **Purpose**: Tests Semantic Kernel with specific configuration
- **When to use**: To verify AI framework integration

#### **`test/test_main_app.py`**
- **Purpose**: Tests the complete application functionality
- **When to use**: End-to-end testing of the entire system

#### **`test/test_all.py`**
- **Purpose**: Runs all tests together
- **When to use**: Comprehensive system verification

### **⚙️ Setup Scripts (CONVENIENCE)**

#### **`setup.ps1` - Environment Setup Script**
- **Purpose**: PowerShell script to set up the development environment
- **What it does**: Installs dependencies, configures environment
- **Platform**: Windows PowerShell

#### **`start.ps1` - Application Launcher**
- **Purpose**: PowerShell script to start the application
- **What it does**: Runs the Chainlit web interface
- **Platform**: Windows PowerShell

## 🔄 **How Everything Works Together**

### **Step 1: Infrastructure Setup (One-time)**
```
terraform/main.tf + variables.tf + terraform.tfvars
    ↓ (terraform apply)
Creates AKS cluster + Azure OpenAI in Azure
```

### **Step 2: Local Environment Setup (One-time)**
```
requirements.txt
    ↓ (pip install -r requirements.txt)
Installs Python packages on your machine
```

### **Step 3: Configuration (One-time)**
```
.env file
    ↓
Contains Azure OpenAI credentials and settings
```

### **Step 4: Running the Application (Every time you use it)**
```
app_ui.py (chainlit run app_ui.py -w)
    ↓ imports and calls
app.py (create_kubernetes_discovery_agent())
    ↓ reads config from
.env file
    ↓ uses functions from
utilities.py
    ↓ spawns subprocess
mcp-server-kubernetes (Node.js)
    ↓ connects to
Your AKS cluster in Azure
```

## 🎮 **User Journey**

### **What You See:**
1. **Open browser** → `http://localhost:8000`
2. **See chat interface** → Similar to ChatGPT
3. **Type questions** → "Show me all namespaces in my cluster"
4. **Get AI responses** → Intelligent analysis of your Kubernetes cluster

### **What Happens Behind the Scenes:**
1. **Your question** goes to `app_ui.py`
2. **app_ui.py** sends it to the AI agent in `app.py`
3. **AI agent** uses Azure OpenAI to understand your question
4. **AI agent** uses MCP server to query your AKS cluster
5. **AI agent** combines cluster data with AI analysis
6. **Response** is sent back through `app_ui.py` to your browser

## 🔧 **External Dependencies**

### **Cloud Services (Running in Azure):**
- **Azure OpenAI Service**: Provides the AI intelligence
- **AKS Cluster**: Your Kubernetes cluster to analyze
- **Azure Container Registry**: Stores container images

### **Local Tools (Running on your machine):**
- **Python**: Programming language runtime
- **Node.js**: Runtime for MCP server
- **kubectl**: Kubernetes command-line tool
- **mcp-server-kubernetes**: Node.js package for Kubernetes discovery

### **Python Packages (Installed via pip):**
- **semantic-kernel**: Microsoft's AI orchestration framework
- **chainlit**: Web interface framework
- **azure-identity**: Azure authentication library
- **python-dotenv**: Environment variable management

## 💾 **Data Flow**

### **Configuration Data:**
```
.env → app.py → Azure OpenAI Service
terraform.tfvars → main.tf → Azure Resources
```

### **Runtime Data:**
```
Your Questions → app_ui.py → app.py → Azure OpenAI → AI Response
Cluster Queries → MCP Server → kubectl → AKS Cluster → Cluster Data
```

### **Output Data:**
```
AI Responses → Browser (via app_ui.py)
Cluster Reports → utilities.py → ./ClusterReports/ folder
```

## 📊 **File Criticality Levels**

### **🔴 CRITICAL (Application won't work without these):**
- `app.py`
- `app_ui.py`
- `.env`
- `requirements.txt`

### **🟡 IMPORTANT (Needed for full functionality):**
- `utilities.py`
- `terraform/main.tf`
- External: `mcp-server-kubernetes`, `kubectl`

### **🟢 HELPFUL (Makes life easier):**
- All test files
- Documentation files
- Setup scripts

## 🚀 **Getting Started Summary**

### **For First-Time Setup:**
1. **Deploy infrastructure**: `terraform apply`
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Configure credentials**: Update `.env` file
4. **Install MCP server**: `npm install -g mcp-server-kubernetes`
5. **Configure kubectl**: `az aks get-credentials`

### **For Daily Usage:**
1. **Start application**: `chainlit run app_ui.py -w`
2. **Open browser**: Go to `http://localhost:8000`
3. **Chat with AI**: Ask questions about your Kubernetes cluster

## 🎯 **Success Indicators**

### **Everything is working when:**
- ✅ Chainlit web interface loads at `http://localhost:8000`
- ✅ AI agent responds to your questions
- ✅ Cluster information is retrieved and displayed
- ✅ Reports can be generated and saved

### **Troubleshooting Resources:**
- Test files in `test/` folder
- Documentation in `docs/` folder
- Azure CLI commands for cluster connectivity
- Error messages in terminal output

This solution combines **local AI processing** with **cloud infrastructure** to provide an intelligent interface for exploring your Kubernetes clusters! 🎉
