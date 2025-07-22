#!/usr/bin/env python3
"""
Comprehensive test suite to verify all components are working correctly
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def run_all_tests():
    """Run all tests to verify the system is ready"""
    
    print("🧪 Running Comprehensive Test Suite")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: REST API Connection
    print("\n1️⃣ Testing REST API Connection...")
    total_tests += 1
    try:
        exec(open('test/test_rest_api.py').read())
        tests_passed += 1
        print("✅ REST API test PASSED")
    except Exception as e:
        print(f"❌ REST API test FAILED: {e}")
    
    # Test 2: Semantic Kernel Explicit Settings
    print("\n2️⃣ Testing Semantic Kernel with Explicit Settings...")
    total_tests += 1
    try:
        result = await run_test_file('test/test_sk_explicit_settings.py')
        if result:
            tests_passed += 1
            print("✅ Semantic Kernel test PASSED")
        else:
            print("❌ Semantic Kernel test FAILED")
    except Exception as e:
        print(f"❌ Semantic Kernel test FAILED: {e}")
    
    # Test 3: Main Application
    print("\n3️⃣ Testing Main Application...")
    total_tests += 1
    try:
        result = await run_test_file('test/test_main_app.py')
        if result:
            tests_passed += 1
            print("✅ Main Application test PASSED")
        else:
            print("❌ Main Application test FAILED")
    except Exception as e:
        print(f"❌ Main Application test FAILED: {e}")
    
    # Test 4: OpenAI Connection
    print("\n4️⃣ Testing Azure OpenAI Connection...")
    total_tests += 1
    try:
        result = await run_test_file('test/test_openai_connection.py')
        if result:
            tests_passed += 1
            print("✅ Azure OpenAI Connection test PASSED")
        else:
            print("❌ Azure OpenAI Connection test FAILED")
    except Exception as e:
        print(f"❌ Azure OpenAI Connection test FAILED: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Tests Passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED! System is ready for deployment.")
        print("\n🚀 NEXT STEPS:")
        print("1. Deploy the application to AKS")
        print("2. Test Kubernetes discovery functionality")
        print("3. Generate cluster reports")
        return True
    else:
        print(f"⚠️  {total_tests - tests_passed} test(s) failed. Please fix before proceeding.")
        return False

async def run_test_file(test_file):
    """Helper to run a test file and capture result"""
    try:
        # Import and run the test
        test_module = test_file.replace('/', '.').replace('\\', '.').replace('.py', '')
        exec(f"import {test_module}")
        return True
    except Exception as e:
        print(f"Error running {test_file}: {e}")
        return False

def print_environment_status():
    """Print current environment configuration"""
    print("\n🔧 ENVIRONMENT CONFIGURATION")
    print("=" * 60)
    print(f"Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT', 'Not set')}")
    print(f"Deployment: {os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'Not set')}")
    print(f"API Version: {os.getenv('AZURE_OPENAI_API_VERSION', 'Not set')}")
    api_key = os.getenv('AZURE_OPENAI_API_KEY', 'Not set')
    if api_key and api_key != 'Not set':
        print(f"API Key: {'*' * 10}...{api_key[-4:]}")
    else:
        print("API Key: Not set")

if __name__ == "__main__":
    print_environment_status()
    result = asyncio.run(run_all_tests())
    
    if result:
        print("\n🎯 SYSTEM STATUS: READY FOR PRODUCTION")
        sys.exit(0)
    else:
        print("\n❌ SYSTEM STATUS: NEEDS ATTENTION")
        sys.exit(1)
