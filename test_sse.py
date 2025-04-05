from mcp import ClientSession
from mcp.client.sse import sse_client


server_url = "http://localhost:8080/sse"


async def connect():
    _streams_context = sse_client(url=server_url)
    streams = await _streams_context.__aenter__()

    _session_context = ClientSession(*streams)
    session: ClientSession = await _session_context.__aenter__()

    # Initialize
    await session.initialize()

    print(session)
    # List available tools to verify connection
    print("Initialized SSE client...")
    print("Listing tools...")
    response = await session.list_tools()
    tools = response.tools
    print("\nConnected to server with tools:", [tool.name for tool in tools])

    return tools


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(connect())
