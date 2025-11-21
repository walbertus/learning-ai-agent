import asyncio
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage, SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient


async def main():
    mcp_client = MultiServerMCPClient(
        {
            "weather": {
                "transport": "streamable_http",
                "url": "http://localhost:8000/mcp",
            }
        }
    )

    tools = await mcp_client.get_tools()

    llm = ChatOllama(
        model="qwen3:8b",
        reasoning=True,
    )

    agent = create_agent(
        model=llm,
        tools=tools,
        debug=False,
        system_prompt="You are a helpful assistant called Wembo.",
        name="Wembo",
    )

    messages = {
        "messages": [
            SystemMessage(content="be friendly"),
            HumanMessage(content="what is the weather in BSD?"),
        ],
    }

    response = await agent.ainvoke(messages)

    for message in response["messages"]:
        match message:
            case AIMessage():
                print(
                    "AIReasoning:",
                    message.additional_kwargs.get("reasoning_content", ""),
                )
                if message.content.strip():
                    print("AIMessage:", message.content)
            case HumanMessage():
                print("HumanMessage:", message.content)
            case ToolMessage():
                print("ToolMessage:", message.content)
            case _:
                print("Unknown message type:", message)


if __name__ == "__main__":
    asyncio.run(main())
