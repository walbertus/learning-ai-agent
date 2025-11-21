# Learning AI Agent

Personal repo to build AI agent. Learning technical stuff around AI agent.

## Prerequisites

Install [uv](https://docs.astral.sh/uv/) package manager:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Installation

Install the required dependencies:

```bash
uv install -r requirements.txt
```

## Files

- `main.py` - Main AI agent implementation using LangChain with Ollama
- `weather_server.py` - Weather MCP server using FastMCP

## Usage

### Run the AI Agent

```bash
uv run main.py
```

### Run the Weather MCP Server

```bash
uv run weather_server.py
```
