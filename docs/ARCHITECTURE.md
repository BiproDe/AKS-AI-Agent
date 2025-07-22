# AKS AI Agent Architecture Documentation

## 🏗️ System Architecture Overview

This document explains the architecture of the AKS AI Agent and how different components interact.

## 🔄 Component Architecture

### **Semantic Kernel** 📚
**Semantic Kernel is NOT a separate running application** - it's a **Python library/framework** that runs **inside your Python process**.

```python
# When you run this code:
import semantic_kernel as sk
from semantic_kernel.agents import ChatCompletionAgent

# Semantic Kernel becomes part of YOUR Python process
# It's like importing numpy or pandas - it's a library, not a server
```

### **MCP Server** 🔧  
**MCP Server IS a separate Node.js application** that runs as a **subprocess**.

```python
# When you create this:
kube_discovery_plugin = MCPStdioPlugin(
    name="kubernetes",
    description="Kubernetes discovery plugin", 
    command="npx",                           # Spawns new process
    args=["mcp-server-kubernetes"]           # Node.js app starts
)
await kube_discovery_plugin.__aenter__()    # Subprocess created
```

## 🔄 Process Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    YOUR PYTHON PROCESS                         │
│  ┌─────────────────┐    ┌──────────────────────────────────────┐ │
│  │   Chainlit      │    │        Semantic Kernel               │ │
│  │   (Web Server)  │    │  ┌─────────────┐ ┌─────────────────┐ │ │
│  │                 │◄──►│  │   Agent     │ │  Azure OpenAI   │ │ │
│  │   Port: 8000    │    │  │  Engine     │ │  Connector      │ │ │
│  └─────────────────┘    │  └─────────────┘ └─────────────────┘ │ │
│                         │         │                            │ │
│                         │         ▼                            │ │
│                         │  ┌─────────────┐                     │ │
│                         │  │ MCP Client  │                     │ │
│                         │  │ (Built-in)  │                     │ │
│                         │  └─────────────┘                     │ │
│                         └──────────────────┬─────────────────────┘ │
└─────────────────────────────────────────────┼─────────────────────┘
                                              │ STDIO Communication
                                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                SEPARATE NODE.JS PROCESS                        │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │              mcp-server-kubernetes                          │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │ │
│  │  │   MCP       │ │  kubectl    │ │    Kubernetes API       │ │ │
│  │  │ Protocol    │ │ Commands    │ │    Translations         │ │ │
│  │  │ Handler     │ │             │ │                         │ │ │
│  │  └─────────────┘ └─────────────┘ └─────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                              │
                                              ▼ kubectl calls
                                     ┌─────────────────┐
                                     │  AKS Cluster    │
                                     │   (Azure)       │
                                     └─────────────────┘
```

## 📊 Component Details

| Component | Type | Location | Process |
|-----------|------|----------|---------|
| **Chainlit** | Web Framework | Your Python process | Main process |
| **Semantic Kernel** | AI Framework | Your Python process | Main process |
| **Azure OpenAI** | Cloud Service | Azure | Remote API |
| **MCP Client** | Library | Your Python process | Main process |
| **MCP Server** | Node.js App | Your machine | **Subprocess** |
| **kubectl** | CLI Tool | Your machine | Called by MCP server |
| **AKS Cluster** | Kubernetes | Azure | Remote service |

## 🔍 Process Lifecycle

### **1. When You Start the Agent:**
```bash
chainlit run app_ui.py -w
```

### **2. What Happens:**
```python
# Step 1: Python process starts
# Step 2: Semantic Kernel initializes (in-process)
# Step 3: Chainlit web server starts (in-process, port 8000)
# Step 4: MCP plugin creates subprocess:
subprocess.run(["npx", "mcp-server-kubernetes"])  # New Node.js process

# Step 5: Communication established:
# Python ←→ STDIO ←→ Node.js ←→ kubectl ←→ AKS
```

## 🎯 Key Differences

### **Semantic Kernel (Library)**
- ✅ **In-process**: Runs inside your Python application
- ✅ **Memory sharing**: Direct access to Python variables
- ✅ **Fast**: No inter-process communication overhead
- ✅ **Lifecycle**: Lives and dies with your Python process

### **MCP Server (Application)**  
- 🔄 **Subprocess**: Separate Node.js process
- 🔄 **IPC**: Communication via STDIO pipes
- 🔄 **Isolated**: Own memory space, own lifecycle
- 🔄 **Restartable**: Can crash/restart independently

## 💡 Why This Architecture?

1. **Language Separation**: 
   - Semantic Kernel (Python) for AI orchestration
   - MCP Server (Node.js) for Kubernetes expertise

2. **Process Isolation**:
   - If MCP server crashes, Python process continues
   - Different technology stacks can be used

3. **Reusability**:
   - Same MCP server can be used by different AI frameworks
   - Semantic Kernel can use different MCP servers

## 💻 System Requirements

### **Minimum Requirements**

| Component | Requirement | Reason |
|-----------|-------------|---------|
| **OS** | Windows 10/11, macOS 10.15+, Linux | Cross-platform support |
| **RAM** | 8 GB | Semantic Kernel + Chainlit + Node.js processes |
| **CPU** | 4 cores | Concurrent processing (Python + Node.js + kubectl) |
| **Storage** | 2 GB free space | Dependencies + logs + reports |
| **Network** | Stable internet | Azure OpenAI + AKS cluster access |

### **Recommended Requirements**

| Component | Recommendation | Benefit |
|-----------|----------------|----------|
| **RAM** | 16 GB+ | Smooth operation with large cluster data |
| **CPU** | 8 cores+ | Faster processing of cluster analysis |
| **Storage** | 10 GB+ SSD | Better I/O for kubectl operations |
| **Network** | 50+ Mbps | Faster cluster data retrieval |

## 📋 Resource Usage During Operation

### **Local Processes**
```
┌─────────────────┬──────────┬─────────┬─────────────┐
│ Process         │ RAM      │ CPU     │ Network     │
├─────────────────┼──────────┼─────────┼─────────────┤
│ Python (venv)   │ 200-500MB│ 10-30%  │ Minimal     │
│ Chainlit        │ 100-300MB│ 5-15%   │ Local only  │
│ MCP Server      │ 50-150MB │ 5-10%   │ None        │
│ kubectl         │ 20-50MB  │ 1-5%    │ To AKS      │
│ Browser         │ 100-200MB│ 5-10%   │ To Chainlit │
├─────────────────┼──────────┼─────────┼─────────────┤
│ **Total**       │ **~1GB** │ **~50%**│ **Light**   │
└─────────────────┴──────────┴─────────┴─────────────┘
```

### **Cloud Resources**
```
┌─────────────────┬─────────────┬──────────────┐
│ Azure Service   │ Cost/Month  │ Usage        │
├─────────────────┼─────────────┼──────────────┤
│ AKS Cluster     │ $70-200     │ 2-3 nodes    │
│ Azure OpenAI    │ $20-100     │ Per token    │
│ Container Reg   │ $5-20       │ Basic tier   │
│ Networking      │ $10-30      │ Egress       │
├─────────────────┼─────────────┼──────────────┤
│ **Total**       │ **$105-350**│ **Variable** │
└─────────────────┴─────────────┴──────────────┘
```

## 🔧 Troubleshooting

### **Common Issues**

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

## 🚀 Performance Optimization

### **For Better Performance**
1. **Use SSD storage** for faster kubectl operations
2. **Close unused applications** during heavy cluster analysis
3. **Use Azure regions close to you** for lower latency
4. **Configure kubectl context switching** for multiple clusters

### **For Cost Optimization**
1. **Use smaller AKS node sizes** for testing
2. **Enable cluster autoscaling** to reduce idle costs
3. **Use Azure OpenAI shared capacity** initially
4. **Stop AKS cluster** when not in use

## 📝 Summary

**Semantic Kernel** is a **library running in your Python process**, while **MCP Server** is a **separate Node.js application/subprocess**. Only the MCP server runs as an independent application!
