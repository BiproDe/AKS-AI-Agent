"""
Simple test script to verify MCP server and dependencies
"""
import sys
import subprocess
import asyncio
import psutil
import platform

def check_system_requirements():
    """Check system requirements"""
    print("🔍 Checking System Requirements...")
    
    # RAM
    ram_gb = psutil.virtual_memory().total / (1024**3)
    print(f"📊 RAM: {ram_gb:.1f} GB {'✅' if ram_gb >= 8 else '❌ Need 8GB+'}")
    
    # CPU
    cpu_count = psutil.cpu_count()
    print(f"⚡ CPU Cores: {cpu_count} {'✅' if cpu_count >= 4 else '❌ Need 4+'}")
    
    # OS
    os_info = f"{platform.system()} {platform.release()}"
    print(f"💻 OS: {os_info}")
    
    # Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    python_ok = (sys.version_info.major, sys.version_info.minor) >= (3, 8)
    print(f"🐍 Python: {python_version} {'✅' if python_ok else '❌ Need 3.8+'}")
    
    return ram_gb >= 8 and cpu_count >= 4 and python_ok

def test_mcp_server():
    """Test if MCP server is accessible"""
    try:
        print("🔍 Testing MCP server installation...")
        
        # Test if npx command works
        result = subprocess.run(
            ["npx", "--version"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if result.returncode == 0:
            print(f"✅ npx version: {result.stdout.strip()}")
        else:
            print("❌ npx not working")
            return False
            
        # Test if mcp-server-kubernetes is accessible
        result = subprocess.run(
            ["npx", "mcp-server-kubernetes", "--version"], 
            capture_output=True, 
            text=True, 
            timeout=15
        )
        
        if result.returncode == 0:
            print(f"✅ MCP server version: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ MCP server error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Command timed out - this might indicate a hanging process")
        return False
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        return False

def test_imports():
    """Test if all required packages are importable"""
    try:
        print("\n🔍 Testing Python imports...")
        
        import semantic_kernel
        print(f"✅ semantic-kernel: {semantic_kernel.__version__}")
        
        import chainlit
        print(f"✅ chainlit: {chainlit.__version__}")
        
        from semantic_kernel.connectors.mcp import MCPStdioPlugin
        print("✅ MCPStdioPlugin imported successfully")
        
        import azure.identity
        print("✅ azure-identity imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

async def test_mcp_plugin():
    """Test MCP plugin initialization (without kubernetes cluster)"""
    try:
        print("\n🔍 Testing MCP plugin initialization...")
        
        from semantic_kernel.connectors.mcp import MCPStdioPlugin
        
        # Create plugin but don't start it yet
        plugin = MCPStdioPlugin(
            name="kubernetes",
            description="Kubernetes discovery plugin",
            command="npx",
            args=["mcp-server-kubernetes"]
        )
        
        print("✅ MCP plugin created successfully")
        print("⚠️ Not starting plugin (requires kubernetes cluster)")
        
        return True
        
    except Exception as e:
        print(f"❌ MCP plugin error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting AKS AI Agent Tests\n")
    
    # Test 0: System Requirements
    if not check_system_requirements():
        print("⚠️ System requirements not met, but continuing...")
    
    # Test 1: Imports
    if not test_imports():
        sys.exit(1)
        
    # Test 2: MCP Server
    if not test_mcp_server():
        print("\n⚠️ MCP server test failed, but we can continue")
        
    # Test 3: MCP Plugin
    asyncio.run(test_mcp_plugin())
    
    print("\n🎉 Basic tests completed!")
    print("\nNext steps:")
    print("1. Configure .env file with Azure OpenAI credentials")
    print("2. Deploy AKS cluster or connect to existing cluster")
    print("3. Run the full agent with: chainlit run app_ui.py -w")
