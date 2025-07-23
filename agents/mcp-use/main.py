import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient
from langchain_google_genai import ChatGoogleGenerativeAI


async def main():
    # Load environment variables
    load_dotenv()

    # Create MCPClient from config file
    client = MCPClient.from_config_file(
        os.path.join(os.path.dirname(__file__), "browser_mcp.json")
    )

    # Create LLM
    # llm = ChatOpenAI(model="gpt-4o")
    # Alternative models:
    # llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
    # llm = ChatGroq(model="llama3-8b-8192")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY")
    )

    # Create agent with the client
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=30,
        system_prompt="You are a helpful assistant. Trả lời bằng tiếng Việt",
    )

    # Run the query
    result = await agent.run(
        "Tìm quán cà phê đẹp quận 2, kèm địa chỉ, đánh gía và số điện thoại, giờ mở cửa",
        max_steps=30,
    )
    print(f"\nResult: {result}")


if __name__ == "__main__":
    asyncio.run(main())
