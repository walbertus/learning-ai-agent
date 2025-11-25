# Learning AI Agent

Personal repo to build AI agent. Learning technical stuff around AI agent.

## Prerequisites

### Python Setup

Install [uv](https://docs.astral.sh/uv/) package manager:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Node.js Setup

For TypeScript/JavaScript implementation:

```bash
# Install dependencies
npm install
# or
yarn install
```

### Milvus Setup

For local development, use Docker Compose to run Milvus:

```bash
docker-compose up -d
```

This will start a Milvus instance at `http://localhost:19530`. The ingester and querier tools are configured to use this endpoint.

### Environment Configuration

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` to set your Milvus connection settings and other configuration options.

## Installation

### Python Dependencies

```bash
uv install -r requirements.txt
```

### TypeScript Dependencies

```bash
npm install
```

## Project Structure

### Python Files
- `tools/ingester.py` - Document ingestion and vector storage using Milvus
- `tools/querier.py` - Query interface for the vector database
- `tools/weather_server.py` - Weather MCP server using FastMCP

### TypeScript Files
- `main.ts` - TypeScript AI agent implementation using LangChain and LangGraph
- `package.json` - Node.js dependencies and scripts
- `tsconfig.json` - TypeScript configuration

### Other
- `docs/` - Documentation and example files
- `data/` - Data storage directory (vector databases, etc.)
- `docker-compose.yml` - Docker Compose configuration for Milvus

## Usage

### Start Milvus (Required for Ingester/Querier)

Before running the ingester or querier, start Milvus:

```bash
docker-compose up -d
```

To stop Milvus:

```bash
docker-compose down
```

### Run TypeScript Agent

```bash
npm run dev
```

### Run Python MCP Servers

Start the weather server:

```bash
uv run tools/weather_server.py
```

Start the querier server:

```bash
uv run tools/querier.py
```

### Run Document Ingestion

```bash
uv run tools/ingester.py
```
