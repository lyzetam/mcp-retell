# mcp-retell

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Retell AI Voice API as a Python library, LangChain tools, and MCP server. Manage voice agents, initiate phone calls, retrieve transcripts, and browse the voice library -- all from code or an MCP-compatible client.

## Features

**13 tools** across 4 categories:

- **Agents** -- list, get, create, update, delete voice agents
- **Calls** -- create outbound phone calls, list calls, get call details, get call transcripts
- **Phone Numbers** -- list registered numbers, update number configuration
- **Voices** -- list available voices, get voice details

## Installation

```bash
# Core library only
pip install .

# With MCP server
pip install ".[mcp]"

# With LangChain tools
pip install ".[langchain]"

# Everything
pip install ".[all]"
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `RETELL_API_KEY` | Retell API key | (required) |
| `RETELL_BASE_URL` | Retell API base URL | `https://api.retellai.com` |

Create a `.env` file:

```env
RETELL_API_KEY=your-retell-api-key
```

## Quick Start

### MCP Server

```bash
mcp-retell
```

### LangChain Tools

```python
from mcp_retell.langchain_tools import TOOLS, retell_list_agents

# Use individual tools
result = retell_list_agents.invoke({})

# Or pass all tools to an agent
from langchain.agents import AgentExecutor
agent = AgentExecutor(tools=TOOLS, ...)
```

### Python Library

```python
from mcp_retell.client import RetellClient

client = RetellClient()

# Async
agents = await client.get("/list-agents")

# Sync (for LangChain)
agents = client.get_sync("/list-agents")
```

## License

MIT
