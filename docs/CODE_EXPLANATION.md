# AKS AI Agent - Line-by-Line Code Explanation

## 📚 **Purpose of This Document**

This document explains every line of code in the three main Python files of your AKS AI Agent project. It's written for someone with basic Python knowledge who wants to understand exactly how everything works.

---

## 🔧 **File 1: `utilities.py` - Helper Functions**

### **What this file does:**
This file contains helper functions that other parts of the application use. Think of it as a toolbox with useful tools.

### **Line-by-Line Explanation:**

```python
"""
Utility functions for the Kubernetes Discovery Agent
"""
```
- **Lines 1-3**: This is called a "docstring" - it's a comment that describes what the file does
- **Purpose**: Documents that this file contains helper functions for the Kubernetes agent

```python
import os
```
- **Line 4**: Imports Python's built-in `os` module
- **What `os` does**: Provides functions to interact with the operating system (like creating folders, file paths)
- **Why we need it**: To work with file paths and directories

```python
def write_to_file_md(file_path: str, content: str) -> None:
```
- **Line 6**: Defines a function named `write_to_file_md`
- **`def`**: Python keyword to define a function
- **`file_path: str`**: Parameter that expects a string (the path where to save the file)
- **`content: str`**: Parameter that expects a string (what to write in the file)
- **`-> None`**: This function doesn't return anything (None means nothing)
- **Purpose**: This function will save text content to a markdown file

```python
    """
    Write content to a markdown file.
    
    Args:
        file_path (str): Path to the file to write
        content (str): Content to write to the file
    """
```
- **Lines 7-12**: Another docstring that explains what this function does
- **Args section**: Describes what each parameter does
- **Best practice**: Always document your functions so others can understand them

```python
    try:
```
- **Line 13**: Starts a "try block" 
- **What try does**: Attempts to run code, and if there's an error, it catches it
- **Why we use it**: File operations can fail (file not found, no permission, etc.)

```python
        with open(file_path, 'w', encoding='utf-8') as f:
```
- **Line 14**: Opens a file for writing
- **`open()`**: Python built-in function to open files
- **`file_path`**: The location where to save the file
- **`'w'`**: Mode 'w' means "write" (creates new file or overwrites existing)
- **`encoding='utf-8'`**: Ensures the file can handle special characters
- **`as f`**: Creates a variable `f` that represents the opened file
- **`with`**: Ensures the file is properly closed when done (even if error occurs)

```python
            f.write(content)
```
- **Line 15**: Writes the content to the file
- **`f.write()`**: Method to write text to the file
- **`content`**: The text we want to save

```python
        print(f"Successfully wrote content to {file_path}")
```
- **Line 16**: Prints a success message
- **`f"..."`**: F-string formatting - lets you put variables inside strings
- **`{file_path}`**: Inserts the actual file path into the message
- **Purpose**: Lets the user know the file was saved successfully

```python
    except Exception as e:
```
- **Line 17**: Catches any errors that happened in the try block
- **`Exception`**: The general type of error
- **`as e`**: Stores the error information in variable `e`

```python
        print(f"Error writing to file {file_path}: {e}")
        raise
```
- **Lines 18-19**: Handle the error
- **Line 18**: Prints an error message with details
- **Line 19**: `raise` re-throws the error so other parts of the program know something went wrong

**Summary of utilities.py:**
This file has one function that safely saves text to a file. It handles errors gracefully and provides feedback to the user.

---

## 🎨 **File 2: `app_ui.py` - Web Interface**

### **What this file does:**
This creates the web interface (the chat page you see in your browser). It uses a framework called Chainlit to create a ChatGPT-like interface.

### **Line-by-Line Explanation:**

```python
import chainlit as cl 
```
- **Line 1**: Imports the Chainlit framework
- **`as cl`**: Creates a shorter name `cl` instead of typing `chainlit` every time
- **What Chainlit does**: Creates web-based chat interfaces for AI applications

```python
from app import create_kubernetes_discovery_agent
```
- **Line 2**: Imports a specific function from the `app.py` file
- **`from app`**: From the file named `app.py`
- **`import create_kubernetes_discovery_agent`**: Import just this one function
- **Purpose**: This function will create our AI agent

```python
@cl.on_chat_start 
```
- **Line 4**: This is a "decorator" - it tells Chainlit when to run the next function
- **`@cl.on_chat_start`**: Run the next function when someone opens the chat
- **Think of it as**: "When a user visits the website, do this..."

```python
async def start(): 
```
- **Line 5**: Defines an asynchronous function named `start`
- **`async`**: This function can wait for other things to complete (like connecting to Azure)
- **`def start()`**: The function that runs when someone opens the chat

```python
    # Create agent using environment variables
    agent = await create_kubernetes_discovery_agent()
```
- **Line 6**: Comment explaining what the next line does
- **Line 7**: Creates the AI agent
- **`await`**: Wait for the agent to be fully created before continuing
- **`create_kubernetes_discovery_agent()`**: Calls the function from `app.py`
- **Result**: `agent` now contains a working AI agent that can answer Kubernetes questions

```python
    cl.user_session.set("agent", agent)
```
- **Line 8**: Stores the agent for this user's session
- **`cl.user_session`**: Chainlit's way to remember things for each user
- **`.set("agent", agent)`**: Saves the agent with the name "agent"
- **Why**: So we can use the same agent for all messages from this user

```python
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
```
- **Lines 10-32**: Creates a welcome message
- **`welcome_msg = """`**: Multi-line string (three quotes let you write multiple lines)
- **Content**: Instructions for the user on what they can ask
- **Markdown formatting**: `**bold**`, `🎯` emojis make it look nice

```python
    await cl.Message(content=welcome_msg).send()
```
- **Line 33**: Sends the welcome message to the user
- **`cl.Message()`**: Creates a message object
- **`content=welcome_msg`**: The message content is our welcome text
- **`.send()`**: Actually sends the message to the user's browser
- **`await`**: Wait for the message to be sent

```python
@cl.on_message 
```
- **Line 35**: Another decorator - runs when user sends a message
- **Think of it as**: "When the user types something and hits enter, do this..."

```python
async def on_message(message): 
```
- **Line 36**: Function that handles user messages
- **`async`**: Can wait for AI responses (which take time)
- **`message`**: Contains what the user typed

```python
    agent = cl.user_session.get("agent") 
```
- **Line 37**: Gets the AI agent we saved earlier
- **`cl.user_session.get("agent")`**: Retrieves the agent using the name "agent"
- **Purpose**: We need the agent to process the user's question

```python
    if not agent:
        await cl.Message(content="❌ Agent not initialized. Please refresh the page.").send()
        return
```
- **Lines 39-41**: Safety check - what if there's no agent?
- **`if not agent:`**: If agent is None or doesn't exist
- **Line 40**: Send error message to user
- **`return`**: Stop the function here (don't continue)

```python
    try:
```
- **Line 43**: Start error handling (like in utilities.py)
- **Purpose**: AI operations can fail, so we need to catch errors

```python
        # Agent invoke returns an async generator
        response_content = ""
```
- **Line 44**: Comment explaining the next part
- **Line 45**: Creates empty string to collect the AI response
- **Why empty string**: We'll add text to this as we get responses

```python
        async for response in agent.invoke(message.content):
```
- **Line 46**: Ask the AI agent to process the user's message
- **`agent.invoke()`**: Send the question to the AI agent
- **`message.content`**: The actual text the user typed
- **`async for`**: The AI sends responses in chunks, so we loop through them
- **Think of it as**: "For each piece of the AI's response..."

```python
            if hasattr(response, 'content'):
                if hasattr(response.content, 'content'):
                    response_content += str(response.content.content)
                else:
                    response_content += str(response.content)
            else:
                response_content += str(response)
```
- **Lines 47-52**: Extract the actual text from the AI response
- **`hasattr()`**: Checks if an object has a specific property
- **Line 47**: Does the response have a 'content' property?
- **Line 48**: Does the content have another 'content' inside it?
- **Lines 49, 51**: Add the text to our response string
- **`str()`**: Convert to text (in case it's not already text)
- **`+=`**: Add to the existing string

```python
        if response_content:
            await cl.Message(content=response_content).send()
        else:
            await cl.Message(content="❌ No response received from the agent.").send()
```
- **Lines 54-57**: Send the AI's response to the user
- **Line 54**: If we got some response text
- **Line 55**: Send it to the user
- **Lines 56-57**: If no response, send error message

```python
    except Exception as e:
        error_msg = f"❌ Error processing your request: {str(e)}"
        await cl.Message(content=error_msg).send()
```
- **Lines 59-61**: Handle any errors that occurred
- **Line 60**: Create error message with details
- **Line 61**: Send error message to user

**Summary of app_ui.py:**
This file creates a web chat interface. When someone opens the page, it creates an AI agent and shows a welcome message. When they type questions, it sends them to the AI agent and shows the responses.

---

## 🤖 **File 3: `app.py` - Main AI Agent Logic**

### **What this file does:**
This is the "brain" of the application. It creates an AI agent that can understand questions about Kubernetes and use tools to get answers from your AKS cluster.

### **Line-by-Line Explanation:**

```python
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
```
- **Lines 1-10**: Import all the libraries we need
- **`os`**: Operating system functions
- **`semantic_kernel`**: Microsoft's AI framework for building AI agents
- **`AzureChatCompletion`**: Connects to Azure OpenAI service
- **`AzureChatPromptExecutionSettings`**: Configuration for AI responses
- **`MCPStdioPlugin`**: Connects to the Kubernetes discovery tool
- **`ChatCompletionAgent`**: The main AI agent class
- **`kernel_function`**: Decorator to create AI-callable functions
- **`utilities`**: Our helper functions from utilities.py
- **`dotenv`**: Loads configuration from .env file

```python
# Load environment variables
load_dotenv()
```
- **Lines 12-13**: Load configuration from .env file
- **`load_dotenv()`**: Reads .env file and makes values available to `os.getenv()`
- **Purpose**: Gets your Azure OpenAI credentials and settings

```python
REPORT_DIR = os.getenv("REPORT_DIR", "./ClusterReports/")
```
- **Line 15**: Sets the directory where reports will be saved
- **`os.getenv()`**: Gets value from environment variables
- **`"REPORT_DIR"`**: The name of the environment variable
- **`"./ClusterReports/"`**: Default value if environment variable doesn't exist

```python
kube_discovery_plugin = None  # Keep global reference alive
```
- **Line 16**: Creates a global variable to store the Kubernetes plugin
- **`None`**: Initially empty
- **Comment explains**: We need to keep this reference so the plugin doesn't get deleted

```python
class ClusterReportPlugin:
    def __init__(self):
        pass
```
- **Lines 18-20**: Defines a new class for generating reports
- **`class`**: Creates a new type of object
- **`__init__`**: Special function that runs when creating a new instance
- **`pass`**: Does nothing (placeholder)

```python
    @kernel_function(
        name="generate_cluster_summary",
        description="Generate a detailed Markdown summary of the Kubernetes cluster and save it to a file."
    )
```
- **Lines 22-25**: Decorator that makes this function available to the AI agent
- **`@kernel_function`**: Tells Semantic Kernel this function can be called by AI
- **`name`**: What the AI will call this function
- **`description`**: Explains to the AI what this function does

```python
    def generate_cluster_summary(self, summary_markdown: str, save_file: bool) -> str:
```
- **Line 26**: Function that the AI can call to save reports
- **`summary_markdown: str`**: The report content (markdown text)
- **`save_file: bool`**: Whether to save to file (True/False)
- **`-> str`**: Returns a string message

```python
        if save_file:
            os.makedirs(REPORT_DIR, exist_ok=True)
            file_path = os.path.join(REPORT_DIR, "cluster_summary.md")
            util.write_to_file_md(file_path, summary_markdown)
            return f"Cluster summary document generated: `{file_path}`"
        else:
            return summary_markdown
```
- **Lines 27-33**: The function logic
- **Line 27**: If we should save to file
- **Line 28**: Create the reports directory if it doesn't exist
- **Line 29**: Create the full file path
- **Line 30**: Use our utility function to save the file
- **Line 31**: Return success message
- **Lines 32-33**: If not saving, just return the content

```python
async def create_kubernetes_discovery_agent(
    instructions: str = None,
    deployment_name: str = None,
    endpoint: str = None,
    api_key: str = None
) -> ChatCompletionAgent:
```
- **Lines 36-41**: Main function that creates the AI agent
- **`async def`**: Asynchronous function (can wait for things)
- **Parameters**: All optional with default None values
- **`-> ChatCompletionAgent`**: Returns an AI agent object

```python
    """
    Create an agent that uses MCP to discover Kubernetes cluster resources
    and can write a summary document.
    """
```
- **Lines 42-45**: Docstring explaining what this function does

```python
    global kube_discovery_plugin
```
- **Line 47**: Refers to the global variable we defined earlier
- **Purpose**: We need to store the plugin globally so it doesn't get destroyed

```python
    # Use environment variables as defaults
    deployment_name = deployment_name or os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-standard")
    endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
```
- **Lines 49-53**: Get configuration values
- **`or` logic**: Use parameter if provided, otherwise use environment variable
- **`os.getenv()`**: Gets values from .env file
- **Default values**: Some have defaults like "gpt-4o-standard" and "2024-02-01"

```python
    if not endpoint or not api_key:
        raise ValueError("Azure OpenAI endpoint and API key must be provided either as parameters or environment variables")
```
- **Lines 55-56**: Safety check for required values
- **`if not endpoint or not api_key`**: If either is missing
- **`raise ValueError()`**: Stop with an error message

```python
    instructions = instructions or "You are a Kubernetes discovery assistant that helps users explore and assess their Kubernetes clusters. You can discover namespaces, pods, services, deployments, and generate detailed cluster reports."
```
- **Line 58**: Set default instructions for the AI agent
- **Purpose**: Tells the AI what its role is and what it should help with

```python
    kernel = sk.Kernel()
```
- **Line 60**: Creates a Semantic Kernel instance
- **Think of kernel as**: The "brain" that coordinates AI and tools

```python
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
```
- **Lines 62-71**: Connect the AI brain to Azure OpenAI
- **`kernel.add_service()`**: Adds a new capability to the kernel
- **`AzureChatCompletion()`**: Creates connection to Azure OpenAI
- **Parameters**: Uses the configuration we loaded earlier

```python
    # Initialize and start the MCP plugin
    kube_discovery_plugin = MCPStdioPlugin(
        name="kubernetes",
        description="Kubernetes discovery plugin",
        command="npx",
        args=["mcp-server-kubernetes"]
    )
    await kube_discovery_plugin.__aenter__()
```
- **Lines 73-80**: Create and start the Kubernetes discovery tool
- **`MCPStdioPlugin`**: Creates a connection to external tool
- **`command="npx"`**: How to run the tool (Node.js package runner)
- **`args=["mcp-server-kubernetes"]`**: The specific tool to run
- **`await ... __aenter__()`**: Start the tool and wait for it to be ready

```python
    # Register plugins
    kernel.add_plugin(kube_discovery_plugin, plugin_name="kubernetes_discovery_plugin")
    kernel.add_plugin(ClusterReportPlugin(), plugin_name="cluster_report_plugin")
```
- **Lines 82-84**: Give the AI access to tools
- **First plugin**: Kubernetes discovery (external tool)
- **Second plugin**: Report generation (our custom class)
- **Purpose**: Now the AI can use these tools to answer questions

```python
    return ChatCompletionAgent(
        kernel=kernel,
        name="KubernetesDiscoveryAgent",
        description="Discovers Kubernetes namespaces, pods, services, images, and generates cluster summary document.",
        instructions=instructions
    )
```
- **Lines 86-91**: Create and return the final AI agent
- **`ChatCompletionAgent()`**: The main AI agent class
- **`kernel=kernel`**: Give it the brain we configured
- **`name` and `description`**: Identify what this agent does
- **`instructions`**: The AI's role and capabilities

**Summary of app.py:**
This file creates an AI agent that can:
1. Connect to Azure OpenAI for intelligence
2. Use a Kubernetes discovery tool to get cluster information
3. Generate and save reports
4. Answer questions about your Kubernetes cluster

---

## 🔄 **How All Three Files Work Together**

### **The Complete Flow:**

1. **User starts application**: `chainlit run app_ui.py -w`

2. **app_ui.py executes**:
   - Imports `create_kubernetes_discovery_agent` from `app.py`
   - When user opens browser, calls `start()` function
   - `start()` calls `create_kubernetes_discovery_agent()` from `app.py`

3. **app.py executes**:
   - Loads configuration from `.env` file
   - Creates AI agent with Azure OpenAI connection
   - Starts Kubernetes discovery tool
   - Returns configured agent to `app_ui.py`

4. **User types question in browser**:
   - `app_ui.py` receives the message
   - Sends question to AI agent (from `app.py`)
   - AI agent processes question using Azure OpenAI and Kubernetes tools
   - Response sent back to user's browser

5. **If user asks for report**:
   - AI agent calls `generate_cluster_summary()` function
   - Function uses `utilities.py` to save file
   - Report saved to `./ClusterReports/` folder

### **Key Concepts for Beginners:**

- **Import**: Bringing code from other files into your current file
- **Function**: A piece of code that does a specific task
- **Class**: A template for creating objects with specific capabilities
- **Async/Await**: Way to handle operations that take time (like network calls)
- **Decorator**: Special syntax (@something) that modifies how functions work
- **Environment Variables**: Configuration stored in .env file
- **Global Variable**: Variable that can be accessed from anywhere in the file

### **Why This Architecture:**

- **Separation of Concerns**: Each file has a specific job
- **Reusability**: Functions can be used by different parts of the application
- **Maintainability**: Easy to find and fix issues
- **Scalability**: Easy to add new features

This design makes it easy to understand, modify, and extend your AKS AI Agent! 🚀
