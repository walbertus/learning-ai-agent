import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";
import { ChatOllama } from "@langchain/ollama";
import { createReactAgent } from "@langchain/langgraph/prebuilt";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { AIMessage, HumanMessage, SystemMessage } from "@langchain/core/messages";
import { DynamicStructuredTool } from "@langchain/core/tools";
import { z } from "zod";
import { MultiServerMCPClient } from "@langchain/mcp-adapters";

async function main() {
  const client = new MultiServerMCPClient({
    weather: {
      transport: "sse",
      url: "http://localhost:8000/sse",
    },
    knowledge_base: {
      transport: "sse",
      url: "http://localhost:8001/sse",
    }
  });

  const tools = await client.getTools();

  const llm = new ChatOllama({
    model: "qwen3:8b",
    temperature: 0,
  });

  const agent = createReactAgent({
    llm,
    tools,
  });

  const systemMessage = new SystemMessage("You are a helpful assistant called Wembo. Be friendly");
  // const userMessage = new HumanMessage("I want to create ML pipeline, what should I do?");
  // const userMessage = new HumanMessage("What I should not consider to handle data governance for ML data preparation?")
  // const userMessage = new HumanMessage("What I should consider to handle data governance for ML data preparation?")
  const userMessage = new HumanMessage("Help explaining what is CNAI and why it need working group?")

  for await (const chunk of await agent.stream(
    { messages: [systemMessage, userMessage] },
    { streamMode: "updates" }
  )) {
    const [step, content] = Object.entries(chunk)[0];
    console.log(`step: ${step}`);
    console.log(`content: ${JSON.stringify(content, null, 2)}`);
  }

  await client.close();
}

main().catch(console.error);
