import chainlit as cl 
from app import create_kubernetes_discovery_agent

@cl.on_chat_start 
async def start(): 
    # Create agent using environment variables
    agent = await create_kubernetes_discovery_agent()
    cl.user_session.set("agent", agent)
    
    # Send welcome message
    welcome_msg = """
    🎯 **AKS AI Agent** - Kubernetes Discovery Assistant
    
    I can help you explore and analyze your AKS cluster! Here's what I can do:
    
    🔍 **Cluster Discovery:**
    - List namespaces, nodes, pods, services
    - Show deployments and workloads
    - Analyze resource usage
    
    📊 **Reports & Analysis:**
    - Generate cluster summary reports
    - Identify potential issues
    - Provide optimization recommendations
    
    **Try asking me:**
    - "Show me all namespaces in the cluster"
    - "List all pods in the kube-system namespace"
    - "Generate a cluster summary report"
    - "What nodes are running in the cluster?"
    
    How can I help you explore your Kubernetes cluster today?
    """
    await cl.Message(content=welcome_msg).send()

@cl.on_message 
async def on_message(message): 
    agent = cl.user_session.get("agent") 
    
    if not agent:
        await cl.Message(content="❌ Agent not initialized. Please refresh the page.").send()
        return
    
    try:
        # Agent invoke returns an async generator
        response_content = ""
        async for response in agent.invoke(message.content):
            if hasattr(response, 'content'):
                if hasattr(response.content, 'content'):
                    response_content += str(response.content.content)
                else:
                    response_content += str(response.content)
            else:
                response_content += str(response)
        
        if response_content:
            await cl.Message(content=response_content).send()
        else:
            await cl.Message(content="❌ No response received from the agent.").send()
            
    except Exception as e:
        error_msg = f"❌ Error processing your request: {str(e)}"
        await cl.Message(content=error_msg).send() 