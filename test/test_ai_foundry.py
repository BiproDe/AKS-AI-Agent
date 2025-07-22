"""
Test Azure AI Foundry project endpoint
"""
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_ai_foundry_endpoint():
    """Test Azure AI Foundry project endpoint"""
    print("🔍 Testing Azure AI Foundry Project Endpoint...")
    print("=" * 55)
    
    # Get configuration
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
        return False
    
    # Try different URL patterns for AI Foundry
    url_patterns = [
        f"{endpoint.rstrip('/')}/openai/deployments/{deployment_name}/chat/completions?api-version={api_version}",
        f"{endpoint.rstrip('/')}/chat/completions?api-version={api_version}",
        f"{endpoint.rstrip('/')}/deployments/{deployment_name}/chat/completions?api-version={api_version}"
    ]
    
    # Headers
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
        "Authorization": f"Bearer {api_key}"  # Try both auth methods
    }
    
    # Request payload
    payload = {
        "messages": [
            {
                "role": "user",
                "content": "Hello! Please respond with 'AI Foundry connection successful!' if you can hear me."
            }
        ],
        "max_tokens": 50,
        "temperature": 0.1
    }
    
    for i, url in enumerate(url_patterns, 1):
        print(f"🌐 Trying URL Pattern {i}: {url}")
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                message = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                print(f"✅ Response: {message}")
                print(f"\n🎉 AI Foundry test PASSED with URL pattern {i}!")
                return True
            else:
                print(f"❌ Failed: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Error: {str(e)[:100]}...")
        
        print()
    
    return False

if __name__ == "__main__":
    print("🚀 Starting Azure AI Foundry Test\n")
    success = test_ai_foundry_endpoint()
    
    if not success:
        print("\n💡 The model might be deployed in AI Foundry but not accessible via OpenAI API.")
        print("Consider creating a standard Azure OpenAI deployment instead.")
