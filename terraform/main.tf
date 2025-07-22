# Configure the Azure Provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

# Configure the Azure Provider features
provider "azurerm" {
  features {}
}

# Create a resource group
resource "azurerm_resource_group" "aks_rg" {
  name     = var.resource_group_name
  location = var.location

  tags = {
    Environment = var.environment
    Project     = "AKS-AI-Agent"
    Owner       = var.owner
  }
}

# Create Azure Container Registry (ACR)
resource "azurerm_container_registry" "acr" {
  name                = var.acr_name
  resource_group_name = azurerm_resource_group.aks_rg.name
  location            = azurerm_resource_group.aks_rg.location
  sku                 = "Basic"
  admin_enabled       = false

  tags = {
    Environment = var.environment
    Project     = "AKS-AI-Agent"
  }
}

# Create AKS Cluster
resource "azurerm_kubernetes_cluster" "aks" {
  name                = var.cluster_name
  location            = azurerm_resource_group.aks_rg.location
  resource_group_name = azurerm_resource_group.aks_rg.name
  dns_prefix          = "${var.cluster_name}-dns"

  # Default node pool
  default_node_pool {
    name                = "default"
    node_count          = var.node_count
    vm_size             = var.vm_size
    type                = "VirtualMachineScaleSets"
    enable_auto_scaling = true
    min_count           = 1
    max_count           = 2
    os_disk_size_gb     = 30
  }

  # Service Principal for AKS
  identity {
    type = "SystemAssigned"
  }

  # Network profile - Azure CNI for better networking
  network_profile {
    network_plugin     = "azure"
    load_balancer_sku  = "standard"
    outbound_type      = "loadBalancer"
    dns_service_ip     = "10.2.0.10"
    service_cidr       = "10.2.0.0/24"
  }

  # RBAC enabled
  role_based_access_control_enabled = true

  tags = {
    Environment = var.environment
    Project     = "AKS-AI-Agent"
  }
}

# Grant AKS access to ACR
resource "azurerm_role_assignment" "aks_acr_pull" {
  scope                = azurerm_container_registry.acr.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
}

# Output important values
output "resource_group_name" {
  value = azurerm_resource_group.aks_rg.name
}

output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.aks.name
}

output "aks_cluster_id" {
  value = azurerm_kubernetes_cluster.aks.id
}

output "aks_fqdn" {
  value = azurerm_kubernetes_cluster.aks.fqdn
}

output "acr_login_server" {
  value = azurerm_container_registry.acr.login_server
}

output "get_credentials_command" {
  value = "az aks get-credentials --resource-group ${azurerm_resource_group.aks_rg.name} --name ${azurerm_kubernetes_cluster.aks.name}"
}
