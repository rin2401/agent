import sys
import asyncio

sys.path.append("..")

from google.adk.runners import Runner
from google.genai import types
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from agent import root_agent
from dotenv import load_dotenv

load_dotenv()


async def main(user_input):
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()

    app_name = "adk_agent"
    runner = Runner(
        app_name=app_name,
        agent=root_agent,
        session_service=session_service,
        memory_service=memory_service,
    )

    user_id = "test"
    session_id = "test"

    session = session_service.create_session(
        app_name=app_name, user_id=user_id, session_id=session_id
    )

    message = types.Content(role="user", parts=[types.Part.from_text(text=user_input)])

    print(f"User: {user_input}")
    print("-" * 20)

    print("Session:", session)

    final_response = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=message,
    ):
        # print("Event:", event)

        if event.content and event.content.parts:
            if event.content.role == "model":
                for part in event.content.parts:
                    if part.text:
                        final_response += part.text

    print(f"Agent: {final_response}")


if __name__ == "__main__":
    asyncio.run(main("Gia Lai sát nhập với tỉnh nào"))
