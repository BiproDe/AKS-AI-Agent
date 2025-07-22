"""
Test script to verify Azure OpenAI connection with Azure AI Foundry
"""
import os
import asyncio
from dotenv import load_dotenv
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)
from semantic_kernel.contents import ChatHistory
import semantic_kernel as sk

# Load environment variables
load_dotenv()

async def test_azure_openai_connection():
    """Test the Azure OpenAI connection"""
    print("🔍 Testing Azure OpenAI Connection...")
    print("=" * 50)
    
    # Get configuration from environment
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
    
    print(f"📍 Endpoint: {endpoint}")
    print(f"🤖 Deployment: {deployment_name}")
    print(f"📅 API Version: {api_version}")
    print(f"🔑 API Key: {'*' * 10}...{api_key[-4:] if api_key else 'NOT SET'}")
    print()
    
    if not endpoint or not api_key or not deployment_name:
        print("❌ Missing required configuration!")
        print("Please check your .env file")
        return False
    
    try:
        # Create Semantic Kernel
        kernel = sk.Kernel()
        
        # Add Azure OpenAI service
        azure_chat_completion = AzureChatCompletion(
            service_id="test_service",
            deployment_name=deployment_name,
            endpoint=endpoint,
            api_key=api_key,
            api_version=api_version
        )
        
        kernel.add_service(azure_chat_completion)
        print("✅ Azure OpenAI service created successfully")
        
        # Test a simple chat completion
        print("\n🧪 Testing chat completion...")
        
        chat_history = ChatHistory()
        chat_history.add_user_message("Hello! Can you respond with 'Azure OpenAI connection successful!' if you can hear me?")
        
        # Create explicit execution settings
        execution_settings = AzureChatPromptExecutionSettings(
            service_id="azure_openai_chat",
            max_tokens=100,
            temperature=0.7
        )
        
        # Get chat completion
        chat_completion = kernel.get_service(type=AzureChatCompletion)
        response = await chat_completion.get_chat_message_contents(
            chat_history=chat_history,
            settings=execution_settings
        )
        
        if response and len(response) > 0:
            print(f"✅ Response received: {response[0].content}")
            print("\n🎉 Azure OpenAI connection test PASSED!")
            return True
        else:
            print("❌ No response received")
            return False
            
    except Exception as e:
        print(f"❌ Connection test FAILED: {str(e)}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check if the endpoint URL is correct")
        print("2. Verify the API key is valid")
        print("3. Ensure the deployment name matches your Azure AI deployment")
        print("4. Check if the API version is supported")
        return False

if __name__ == "__main__":
    print("🚀 Starting Azure OpenAI Connection Test\n")
    success = asyncio.run(test_azure_openai_connection())
    
    if success:
        print("\n✅ Ready to proceed with the full AKS AI Agent!")
    else:
        print("\n❌ Please fix the configuration before proceeding.")
