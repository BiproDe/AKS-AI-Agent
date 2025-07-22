"""
Simplified Semantic Kernel test
"""
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_simple_sk():
    """Test basic Semantic Kernel functionality"""
    print("🔍 Testing Simplified Semantic Kernel...")
    print("=" * 45)
    
    try:
        from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
        print("✅ AzureChatCompletion imported successfully")
        
        # Get configuration
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
        
        print(f"📍 Endpoint: {endpoint}")
        print(f"🤖 Deployment: {deployment_name}")
        print(f"📅 API Version: {api_version}")
        print()
        
        # Create the service
        chat_completion = AzureChatCompletion(
            service_id="test_service",
            deployment_name=deployment_name,
            endpoint=endpoint,
            api_key=api_key,
            api_version=api_version
        )
        print("✅ AzureChatCompletion service created")
        
        # Try a simple completion
        from semantic_kernel.contents import ChatHistory
        
        chat_history = ChatHistory()
        chat_history.add_user_message("Say 'Hello from Semantic Kernel!'")
        
        print("🚀 Attempting chat completion...")
        
        response = await chat_completion.get_chat_message_contents(
            chat_history=chat_history,
            settings=None
        )
        
        if response and len(response) > 0:
            print(f"✅ Response: {response[0].content}")
            print("\n🎉 Semantic Kernel test PASSED!")
            return True
        else:
            print("❌ No response received")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Simplified Semantic Kernel Test\n")
    success = asyncio.run(test_simple_sk())
    
    if success:
        print("\n✅ Ready to test the full AKS AI Agent!")
    else:
        print("\n❌ Semantic Kernel issue needs to be resolved.")
