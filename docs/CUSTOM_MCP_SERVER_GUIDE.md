# Custom MCP Server Development Guide

## 📋 **Overview**

This guide explains how to create custom MCP (Model Context Protocol) servers to extend your AI agent's capabilities. MCP servers are local code packages that provide specialized tools and functions to AI agents.

## 🧩 **Understanding the Architecture**

### **Semantic Kernel (SDK)**
- **What it is**: Microsoft's AI orchestration SDK
- **Role**: Creates and manages AI agents
- **Language**: Python/C#/.NET libraries
- **Purpose**: AI logic, conversation management, plugin orchestration

### **MCP Server (Local Process)**
- **What it is**: Local Node.js/Python process with specialized tools
- **Role**: Provides specific capabilities to AI agents
- **Language**: Node.js or Python
- **Purpose**: Tool execution, API integration, data access

### **How They Work Together**
```mermaid
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Python App    │    │   MCP Server     │    │   External      │
│  (Semantic      │◄──►│  (Node.js        │◄──►│   Systems       │
│   Kernel SDK)   │    │   Process)       │    │   (APIs/DBs)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
        │                        │                       │
        │                        │                       │
    AI Logic               Tool Execution           Real Data
    Orchestration          & Integration            Sources
```

## ⏱️ **Development Time Estimates**

### **Simple Custom MCP Server: 2-4 hours**
- Basic functionality (file operations, simple API calls)
- 1-3 custom functions
- Basic error handling
- **Examples**: File manager, simple calculators, basic utilities

### **Moderate Custom MCP Server: 1-2 days**
- Complex business logic (database operations, cloud APIs)
- 5-10 custom functions
- Proper error handling and validation
- Testing and documentation
- **Examples**: Database connectors, cloud service managers, monitoring tools

### **Advanced Custom MCP Server: 3-5 days**
- Complex integrations (multiple APIs, advanced processing)
- 10+ functions with complex workflows
- Authentication, security, caching
- Comprehensive testing and documentation
- **Examples**: Enterprise integrations, advanced analytics, multi-service orchestration

## 📁 **MCP Server Structure**

**Important**: MCP servers are **code packages**, not remote servers! Users install and run them locally.

### **Basic Project Structure**
```
my-custom-mcp-server/
├── package.json          # Node.js dependencies and metadata
├── index.js              # Main MCP server entry point
├── src/
│   ├── handlers.js       # Your custom function implementations
│   ├── utils.js          # Helper utilities and common functions
│   └── config.js         # Configuration and settings
├── tests/
│   ├── handlers.test.js  # Unit tests for your functions
│   └── integration.test.js # Integration tests
├── README.md             # Installation and usage instructions
├── .gitignore            # Git ignore file
└── examples/
    └── usage-example.js  # Example of how to use your MCP server
```

## 🛠️ **Step-by-Step Development Process**

### **Step 1: Initialize Your MCP Server Project**

```bash
# Create new directory
mkdir my-custom-mcp-server
cd my-custom-mcp-server

# Initialize package.json
npm init -y

# Install MCP SDK
npm install @modelcontextprotocol/sdk

# Create basic structure
mkdir src tests examples
touch index.js src/handlers.js src/utils.js README.md
```

### **Step 2: Create package.json**

```json
{
  "name": "my-custom-mcp-server",
  "version": "1.0.0",
  "description": "Custom MCP server for [your use case]",
  "main": "index.js",
  "type": "module",
  "bin": {
    "my-custom-mcp": "./index.js"
  },
  "scripts": {
    "start": "node index.js",
    "test": "jest",
    "dev": "node --watch index.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.4.0"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  },
  "keywords": ["mcp", "ai-agent", "tools", "your-domain"],
  "author": "Your Name",
  "license": "MIT"
}
```

### **Step 3: Implement Main MCP Server (index.js)**

```javascript
#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { FileManagerHandlers } from './src/handlers.js';

class CustomMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'my-custom-mcp-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.handlers = new FileManagerHandlers();
    this.setupHandlers();
  }

  setupHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'list_files',
            description: 'List files in a directory',
            inputSchema: {
              type: 'object',
              properties: {
                directory: {
                  type: 'string',
                  description: 'Directory path to list files from',
                  default: '.'
                }
              }
            }
          },
          {
            name: 'read_file',
            description: 'Read contents of a file',
            inputSchema: {
              type: 'object',
              properties: {
                filepath: {
                  type: 'string',
                  description: 'Path to the file to read'
                }
              },
              required: ['filepath']
            }
          },
          {
            name: 'create_report',
            description: 'Create a markdown report',
            inputSchema: {
              type: 'object',
              properties: {
                title: {
                  type: 'string',
                  description: 'Report title'
                },
                content: {
                  type: 'string',
                  description: 'Report content'
                }
              },
              required: ['title', 'content']
            }
          }
        ]
      };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'list_files':
            return await this.handlers.listFiles(args.directory || '.');
          
          case 'read_file':
            return await this.handlers.readFile(args.filepath);
          
          case 'create_report':
            return await this.handlers.createReport(args.title, args.content);
          
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          content: [
            {
              type: 'text',
              text: `Error executing ${name}: ${error.message}`
            }
          ],
          isError: true
        };
      }
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Custom MCP Server running on stdio');
  }
}

// Start the server
const server = new CustomMCPServer();
server.run().catch(console.error);
```

### **Step 4: Implement Handlers (src/handlers.js)**

```javascript
import fs from 'fs/promises';
import path from 'path';
import { validatePath, formatFileList } from './utils.js';

export class FileManagerHandlers {
  async listFiles(directory) {
    try {
      // Validate and sanitize the directory path
      const safePath = validatePath(directory);
      
      const files = await fs.readdir(safePath, { withFileTypes: true });
      const fileList = formatFileList(files, safePath);
      
      return {
        content: [
          {
            type: 'text',
            text: `Files in ${safePath}:\n\n${fileList}`
          }
        ]
      };
    } catch (error) {
      throw new Error(`Failed to list files in ${directory}: ${error.message}`);
    }
  }

  async readFile(filepath) {
    try {
      const safePath = validatePath(filepath);
      const stats = await fs.stat(safePath);
      
      if (!stats.isFile()) {
        throw new Error(`${filepath} is not a file`);
      }
      
      const content = await fs.readFile(safePath, 'utf-8');
      
      return {
        content: [
          {
            type: 'text',
            text: `Content of ${filepath}:\n\n${content}`
          }
        ]
      };
    } catch (error) {
      throw new Error(`Failed to read file ${filepath}: ${error.message}`);
    }
  }

  async createReport(title, content) {
    try {
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const filename = `report_${timestamp}.md`;
      
      const markdown = this.generateMarkdown(title, content);
      
      await fs.writeFile(filename, markdown);
      
      return {
        content: [
          {
            type: 'text',
            text: `✅ Report created successfully: ${filename}\n\nLocation: ${path.resolve(filename)}`
          }
        ]
      };
    } catch (error) {
      throw new Error(`Failed to create report: ${error.message}`);
    }
  }

  generateMarkdown(title, content) {
    return `# ${title}

${content}

---

**Report Details:**
- Generated: ${new Date().toISOString()}
- Generator: Custom MCP Server v1.0.0

`;
  }
}
```

### **Step 5: Create Utilities (src/utils.js)**

```javascript
import path from 'path';

export function validatePath(inputPath) {
  // Basic security: prevent directory traversal attacks
  const normalizedPath = path.normalize(inputPath);
  
  if (normalizedPath.includes('..')) {
    throw new Error('Directory traversal not allowed');
  }
  
  return normalizedPath;
}

export function formatFileList(files, directory) {
  if (files.length === 0) {
    return '(empty directory)';
  }
  
  const formatted = files.map(file => {
    const icon = file.isDirectory() ? '📁' : '📄';
    const type = file.isDirectory() ? 'DIR' : 'FILE';
    return `${icon} ${file.name} (${type})`;
  });
  
  return formatted.join('\n');
}

export function sanitizeFilename(filename) {
  return filename.replace(/[^a-z0-9.-]/gi, '_').toLowerCase();
}
```

## 📦 **Distribution Methods**

### **Method 1: NPM Package (Recommended)**

```bash
# 1. Create account on npmjs.com
# 2. Login to NPM
npm login

# 3. Publish your package
npm publish

# 4. Users install globally
npm install -g my-custom-mcp-server
```

### **Method 2: GitHub Repository**

```bash
# 1. Create GitHub repository
# 2. Push your code
git init
git add .
git commit -m "Initial custom MCP server"
git remote add origin https://github.com/yourusername/custom-mcp-server
git push -u origin main

# 3. Users install from GitHub
npm install -g https://github.com/yourusername/custom-mcp-server
```

### **Method 3: Direct Code Sharing**

```bash
# 1. Share the project folder
# 2. Users navigate to folder and install
cd custom-mcp-server
npm install -g .
```

## 🔧 **Integration with AI Agents**

### **How Users Add Your MCP Server to Their Agent**

```python
# In their app.py (like your current AKS AI Agent)
from semantic_kernel.agents.plugins.mcp import MCPPlugin

# Add your custom MCP server
custom_mcp_plugin = MCPPlugin(
    server_command=["my-custom-mcp"],  # The command from package.json bin
    server_parameters={}
)

# Add to kernel
kernel.add_plugin(custom_mcp_plugin, plugin_name="file_manager")

# Now AI agent can use your tools!
# Example user query: "List files in the current directory"
# Example user query: "Create a report titled 'System Analysis' with content about our infrastructure"
```

## 🎯 **Real-World Custom MCP Server Ideas**

### **1. Database Operations MCP Server**
**Time**: 1-2 days
**Functions**:
- `execute_query(sql, database)`
- `get_table_schema(table_name)`
- `backup_database(database_name)`
- `analyze_performance(query)`

### **2. Cloud Resource Management MCP Server**
**Time**: 2-3 days
**Functions**:
- `list_azure_resources(resource_group)`
- `analyze_costs(subscription_id, time_range)`
- `scale_service(service_name, scale_factor)`
- `check_service_health(service_name)`

### **3. Business Intelligence MCP Server**
**Time**: 2-4 days
**Functions**:
- `generate_sales_report(date_range)`
- `calculate_kpis(department)`
- `forecast_trends(metric, periods)`
- `create_dashboard(metrics[])`

### **4. DevOps Automation MCP Server**
**Time**: 1-3 days
**Functions**:
- `deploy_application(app_name, environment)`
- `rollback_deployment(app_name, version)`
- `check_pipeline_status(pipeline_id)`
- `trigger_build(repository, branch)`

## 📝 **Best Practices**

### **Security**
- ✅ Validate all input parameters
- ✅ Sanitize file paths to prevent directory traversal
- ✅ Use environment variables for sensitive data
- ✅ Implement proper error handling
- ✅ Log security events

### **Error Handling**
- ✅ Catch and handle all exceptions
- ✅ Provide meaningful error messages
- ✅ Return consistent error response format
- ✅ Don't expose internal system details in errors

### **Performance**
- ✅ Use async/await for I/O operations
- ✅ Implement caching where appropriate
- ✅ Add timeouts for external API calls
- ✅ Optimize for common use cases

### **Documentation**
- ✅ Write comprehensive README.md
- ✅ Include installation instructions
- ✅ Provide usage examples
- ✅ Document all function parameters
- ✅ Add troubleshooting section

## 🚀 **Testing Your MCP Server**

### **Unit Tests (tests/handlers.test.js)**

```javascript
import { jest } from '@jest/globals';
import { FileManagerHandlers } from '../src/handlers.js';
import fs from 'fs/promises';

// Mock the fs module
jest.mock('fs/promises');

describe('FileManagerHandlers', () => {
  let handlers;

  beforeEach(() => {
    handlers = new FileManagerHandlers();
    jest.clearAllMocks();
  });

  test('listFiles should return formatted file list', async () => {
    // Mock fs.readdir
    fs.readdir.mockResolvedValue([
      { name: 'file1.txt', isDirectory: () => false },
      { name: 'folder1', isDirectory: () => true }
    ]);

    const result = await handlers.listFiles('.');
    
    expect(result.content[0].text).toContain('📄 file1.txt (FILE)');
    expect(result.content[0].text).toContain('📁 folder1 (DIR)');
  });

  test('readFile should return file content', async () => {
    fs.stat.mockResolvedValue({ isFile: () => true });
    fs.readFile.mockResolvedValue('Hello, World!');

    const result = await handlers.readFile('test.txt');
    
    expect(result.content[0].text).toContain('Hello, World!');
  });
});
```

### **Integration Testing**

```bash
# Test your MCP server manually
node index.js

# Test with MCP client tools
npm install -g @modelcontextprotocol/inspector
mcp-inspector my-custom-mcp
```

## 📚 **Advanced Features**

### **Authentication & Configuration**

```javascript
// Add authentication support
class AuthenticatedMCPServer extends CustomMCPServer {
  constructor() {
    super();
    this.apiKey = process.env.API_KEY;
    this.baseUrl = process.env.BASE_URL || 'https://api.example.com';
  }

  async authenticatedRequest(endpoint, options = {}) {
    return fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
        ...options.headers
      }
    });
  }
}
```

### **Caching & Performance**

```javascript
// Add simple caching
class CachedMCPServer extends CustomMCPServer {
  constructor() {
    super();
    this.cache = new Map();
    this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
  }

  async cachedRequest(key, fetcher) {
    const cached = this.cache.get(key);
    
    if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
      return cached.data;
    }

    const data = await fetcher();
    this.cache.set(key, { data, timestamp: Date.now() });
    return data;
  }
}
```

## 🎉 **Conclusion**

Creating custom MCP servers allows you to:
- ✅ **Extend AI agent capabilities** with domain-specific tools
- ✅ **Integrate with existing systems** (databases, APIs, services)
- ✅ **Share reusable components** across different AI projects
- ✅ **Build specialized workflows** for your business needs
- ✅ **Create a marketplace** of AI agent tools

**Remember**: MCP servers are local code packages that users install and run on their machines, not remote services. This approach provides security, performance, and flexibility for AI agent ecosystems.

**Next Steps**: Start with a simple MCP server, test it thoroughly, and gradually add more sophisticated features based on your specific use cases and user feedback.
