import os
import asyncio
from dotenv import load_dotenv

# from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp_use import MCPAgent, MCPClient


async def run_blender_example():
    # Load environment variables
    load_dotenv()

    # Create MCPClient with Blender MCP configuration
    config = {"mcpServers": {"blender": {"command": "uvx", "args": ["blender-mcp"]}}}
    client = MCPClient.from_dict(config)

    # Create LLM
    # llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-pro", api_key=os.getenv("GEMINI_API_KEY")
    )

    # Create agent with the client
    agent = MCPAgent(llm=llm, client=client, max_steps=30)

    try:
        # Run the query
        result = await agent.run(
            "Tạo một hình vuông và 1 hình tam giác và 1 hình tròn",
            max_steps=30,
        )
        print(f"\nResult: {result}")
    finally:
        # Ensure we clean up resources properly
        if client.sessions:
            await client.close_all_sessions()


if __name__ == "__main__":
    asyncio.run(run_blender_example())
