import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents import set_tracing_disabled, function_tool
from tools.weather import get_weather, get_current_time
from dotenv import load_dotenv

load_dotenv()
set_tracing_disabled(True)

tools = [get_weather, get_current_time]
tools = [function_tool(tool) for tool in tools]

client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)

agent = Agent(
    name="weather_time_agent",
    model=model,
    instructions=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=tools,
)


async def main():
    result = await Runner.run(agent, input="Thời tiết ở New York")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
