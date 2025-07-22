"""
Simple REST API test for Azure OpenAI connection
"""
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_azure_openai_rest_api():
    """Test Azure OpenAI using direct REST API calls"""
    print("🔍 Testing Azure OpenAI with REST API...")
    print("=" * 50)
    
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
    
    # Construct the URL
    url = f"{endpoint.rstrip('/')}/openai/deployments/{deployment_name}/chat/completions?api-version={api_version}"
    
    print(f"🌐 Request URL: {url}")
    print()
    
    # Headers
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    
    # Request payload
    payload = {
        "messages": [
            {
                "role": "user",
                "content": "Hello! Please respond with 'Azure OpenAI connection successful!' if you can hear me."
            }
        ],
        "max_tokens": 50,
        "temperature": 0.1
    }
    
    try:
        print("🚀 Sending request...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            message = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"✅ Response: {message}")
            print("\n🎉 Azure OpenAI REST API test PASSED!")
            return True
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"🔍 Error response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Azure OpenAI REST API Test\n")
    success = test_azure_openai_rest_api()
    
    if success:
        print("\n✅ Azure OpenAI is working! The issue might be with Semantic Kernel.")
    else:
        print("\n❌ Azure OpenAI connection failed. Check configuration.")
