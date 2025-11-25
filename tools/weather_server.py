from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="weather",
    port=8000,
)

@mcp.tool()
async def get_weather(city: str) -> str:
    """Get weather for a given city.

    Args:
        city: Name of the city
    """
    # For demonstration, we return a dummy weather response.
    return f"It's always 晴天 in {city}!"


def main():
    # Initialize and run the server
    # The server will be available at http://127.0.0.1:8000/mcp (default streamable_http_path)
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
