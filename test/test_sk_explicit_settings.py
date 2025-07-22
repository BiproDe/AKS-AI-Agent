#!/usr/bin/env python3
"""
Test Semantic Kernel with explicit settings creation to avoid pack_extension_data issue
"""

import asyncio
import os
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)
from dotenv import load_dotenv

async def test_sk_explicit_settings():
    """Test SK with explicit settings creation"""
    print("🚀 Starting Semantic Kernel Test with Explicit Settings")
    
    # Load environment variables
    load_dotenv()
    
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
    
    print(f"📍 Endpoint: {endpoint}")
    print(f"🤖 Deployment: {deployment}")
    print(f"📅 API Version: {api_version}")
    
    try:
        # Create kernel
        kernel = Kernel()
        
        # Add Azure OpenAI chat completion
        kernel.add_service(
            AzureChatCompletion(
                service_id="azure_openai_chat",
                deployment_name=deployment,
                endpoint=endpoint,
                api_key=api_key,
                api_version=api_version
            )
        )
        
        print("✅ Kernel and service created successfully")
        
        # Create explicit execution settings
        execution_settings = AzureChatPromptExecutionSettings(
            service_id="azure_openai_chat",
            max_tokens=100,
            temperature=0.7
        )
        
        print("✅ Execution settings created explicitly")
        
        # Get the chat completion service
        chat_service = kernel.get_service("azure_openai_chat")
        
        # Test with a simple prompt using explicit settings
        from semantic_kernel.contents.chat_history import ChatHistory
        
        chat_history = ChatHistory()
        chat_history.add_user_message("Say hello!")
        
        print("🚀 Attempting chat completion with explicit settings...")
        
        response = await chat_service.get_chat_message_contents(
            chat_history=chat_history,
            settings=execution_settings
        )
        
        if response and len(response) > 0:
            print(f"✅ Success! Response: {response[0].content}")
            print("🎉 Semantic Kernel is working correctly!")
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
    result = asyncio.run(test_sk_explicit_settings())
    if result:
        print("🎯 Semantic Kernel test passed!")
    else:
        print("❌ Semantic Kernel test failed!")
