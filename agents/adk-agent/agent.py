from google.adk.agents import Agent

from tools.weather import get_weather, get_current_time
from google.adk.tools import google_search

tools = [get_weather, get_current_time, google_search]
tools = [google_search]


root_agent = Agent(
    name="adk_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the time and weather in a city, and perform general web searches."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city. You can also use Google Search for other questions."
    ),
    tools=tools,
)
