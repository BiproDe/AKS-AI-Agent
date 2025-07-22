#!/usr/bin/env python3
"""
Test the main app.py to ensure Semantic Kernel integration works after the fix
"""

import asyncio
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_kubernetes_discovery_agent

async def test_main_app():
    """Test the main application functionality"""
    print("🚀 Starting Main App Test")
    print("🔍 Testing Kubernetes Discovery Agent Creation...")
    
    try:
        # Create the agent
        agent = await create_kubernetes_discovery_agent()
        print("✅ Kubernetes Discovery Agent created successfully!")
        
        # Test a simple interaction
        print("🚀 Testing agent interaction...")
        
        # Simple test message
        test_message = "Hello, can you help me understand what you can do with Kubernetes clusters?"
        
        # Agent invoke returns an async generator, so we need to iterate
        response_content = ""
        async for response in agent.invoke(test_message):
            if hasattr(response, 'content'):
                if hasattr(response.content, 'content'):
                    response_content += str(response.content.content)
                else:
                    response_content += str(response.content)
            else:
                response_content += str(response)
        
        if response_content:
            print(f"✅ Agent Response: {response_content[:200]}...")
            print("🎉 Main application is working correctly!")
            return True
        else:
            print("❌ No response content received")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Clean up the global plugin reference if needed
        try:
            import app
            if app.kube_discovery_plugin:
                await app.kube_discovery_plugin.__aexit__(None, None, None)
        except:
            pass

if __name__ == "__main__":
    result = asyncio.run(test_main_app())
    if result:
        print("🎯 Main app test passed!")
    else:
        print("❌ Main app test failed!")
