from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always 晴天 in {city}!"

llm = ChatOllama(
    model="qwen3:0.6b",
    reasoning=True,
)

agent = create_agent(
    model=llm,
    tools=[get_weather],
    debug=False,
    system_prompt="You are a helpful assistant called Wembo.",
    name="Wembo",
)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in BSD?"}]}
)

for message in response["messages"]:
    match message:
        case AIMessage():
            print("AIReasoning:", message.additional_kwargs.get("reasoning_content", ""))
            if message.content.strip():
                print("AIMessage:", message.content)
        case HumanMessage():
            print("HumanMessage:", message.content)
        case ToolMessage():
            print("ToolMessage:", message.content)
        case _:
            print("Unknown message type:", message)
