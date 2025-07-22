# Terraform configuration file for AKS AI Agent
# This file contains variable values for the deployment

resource_group_name = "rg-aks-ai-agent-dev"
location           = "centralindia"
cluster_name       = "aks-ai-agent-cluster"
acr_name          = "acraksiagent001"  # Must be globally unique
node_count        = 2
vm_size           = "Standard_D2s_v3"
environment       = "dev"
owner             = "AI-Agent-Team"
