from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")


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
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
