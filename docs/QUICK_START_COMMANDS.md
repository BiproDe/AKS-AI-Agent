# AKS AI Agent - Quick Start Commands

## 🚀 **Complete Setup & Run Commands**

### **One-Time Setup (First Time Only)**

#### **1. Clone/Download Project**
```bash
# Navigate to your project directory
cd "c:\Users\biprojitdey\OneDrive - Microsoft\Desktop\Learning\AKS AI Agent"
```

#### **2. Install Python Dependencies**
```bash
pip install -r requirements.txt
```

#### **3. Install Node.js Dependencies**
```bash
npm install -g mcp-server-kubernetes
```

#### **4. Deploy Azure Infrastructure**
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

#### **5. Configure kubectl**
```bash
az aks get-credentials --resource-group rg-foundry --name aks-ai-agent-cluster
```

#### **6. Create .env File**
```bash
# Create .env file with your Azure OpenAI credentials
# (Copy from existing .env or set manually)
```

### **Daily Usage (Every Time You Want to Use the Agent)**

#### **1. Start the Application**
```bash
chainlit run app_ui.py -w --port 8000
```

#### **2. Open Browser**
```
http://localhost:8000
```

#### **3. Stop the Application**
```bash
# Press Ctrl+C in terminal or close terminal window
```

### **Testing Commands (Optional)**

#### **1. Test Azure OpenAI Connection**
```bash
python test\test_openai_connection.py
```

#### **2. Test REST API**
```bash
python test\test_rest_api.py
```

#### **3. Test All Components**
```bash
python test\test_all.py
```

### **Troubleshooting Commands**

#### **1. Check AKS Cluster**
```bash
kubectl cluster-info
kubectl get nodes
```

#### **2. Check Azure Resources**
```bash
az account show
az cognitiveservices account list --output table
```

#### **3. Check Python Environment**
```bash
pip list
python --version
```

#### **4. Check Node.js Tools**
```bash
npm list -g mcp-server-kubernetes
node --version
```

### **Infrastructure Management**

#### **1. Stop AKS Cluster (Save Costs)**
```bash
az aks stop --resource-group rg-foundry --name aks-ai-agent-cluster
```

#### **2. Start AKS Cluster**
```bash
az aks start --resource-group rg-foundry --name aks-ai-agent-cluster
```

#### **3. Destroy Infrastructure**
```bash
cd terraform
terraform destroy
```

## 📋 **Command Summary**

### **Setup Once:**
1. `pip install -r requirements.txt`
2. `npm install -g mcp-server-kubernetes`
3. `terraform apply`
4. `az aks get-credentials --resource-group rg-foundry --name aks-ai-agent-cluster`

### **Run Every Time:**
1. `chainlit run app_ui.py -w --port 8000`
2. Open browser: `http://localhost:8000`

### **Stop:**
1. `Ctrl+C` in terminal

That's it! 🎉
