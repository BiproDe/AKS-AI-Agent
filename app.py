import os
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)
from semantic_kernel.connectors.mcp import MCPStdioPlugin
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.functions import kernel_function
import utilities as util
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

REPORT_DIR = os.getenv("REPORT_DIR", "./ClusterReports/")
kube_discovery_plugin = None  # Keep global reference alive

class ClusterReportPlugin:
    def __init__(self):
        pass

    @kernel_function(
        name="generate_cluster_summary",
        description="Generate a detailed Markdown summary of the Kubernetes cluster and save it to a file."
    )
    def generate_cluster_summary(self, summary_markdown: str, save_file: bool) -> str:
        if save_file:
            os.makedirs(REPORT_DIR, exist_ok=True)
            file_path = os.path.join(REPORT_DIR, "cluster_summary.md")
            util.write_to_file_md(file_path, summary_markdown)
            return f"Cluster summary document generated: `{file_path}`"
        else:
            return summary_markdown


async def create_kubernetes_discovery_agent(
    instructions: str = None,
    deployment_name: str = None,
    endpoint: str = None,
    api_key: str = None
) -> ChatCompletionAgent:
    """
    Create an agent that uses MCP to discover Kubernetes cluster resources
    and can write a summary document.
    """

    global kube_discovery_plugin

    # Use environment variables as defaults
    deployment_name = deployment_name or os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-standard")
    endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")

    if not endpoint or not api_key:
        raise ValueError("Azure OpenAI endpoint and API key must be provided either as parameters or environment variables")

    instructions = instructions or "You are a Kubernetes discovery assistant that helps users explore and assess their Kubernetes clusters. You can discover namespaces, pods, services, deployments, and generate detailed cluster reports."

    kernel = sk.Kernel()

    # Add Azure OpenAI completion service
    kernel.add_service(
        AzureChatCompletion(
            service_id="default",
            deployment_name=deployment_name,
            endpoint=endpoint,
            api_key=api_key,
            api_version=api_version
        )
    )

    # Initialize and start the MCP plugin
    kube_discovery_plugin = MCPStdioPlugin(
        name="kubernetes",
        description="Kubernetes discovery plugin",
        command="npx",
        args=["mcp-server-kubernetes"]
    )
    await kube_discovery_plugin.__aenter__()  

    # Register plugins
    kernel.add_plugin(kube_discovery_plugin, plugin_name="kubernetes_discovery_plugin")
    kernel.add_plugin(ClusterReportPlugin(), plugin_name="cluster_report_plugin")

    return ChatCompletionAgent(
        kernel=kernel,
        name="KubernetesDiscoveryAgent",
        description="Discovers Kubernetes namespaces, pods, services, images, and generates cluster summary document.",
        instructions=instructions
    )