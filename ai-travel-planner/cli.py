import warnings
from dotenv import load_dotenv
import asyncio
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.auth.credential_service.in_memory_credential_service import (
    InMemoryCredentialService,
)
from google.adk.apps.app import App
from agent import root_agent

warnings.filterwarnings("ignore", category=UserWarning)
load_dotenv()  # loads .env into os.environ

# Suppress ADK experimental warnings
warnings.filterwarnings("ignore", category=UserWarning, module=r"google\.adk\..*")

# Optional: suppress only function_call concatenation warnings
warnings.filterwarnings("ignore", message=r".*non-text parts in the response.*")

# Task 1: Import Libraries


# Task 9: Connect CLI with Root Agent
async def run_cli():
    artifact_service = InMemoryArtifactService()
    session_service = InMemorySessionService()
    credential_service = InMemoryCredentialService()

    session = await session_service.create_session(
        app_name="TravelPlanner", user_id="user_1"
    )
    app = App(name="TravelPlanner", root_agent=root_agent)

    runner = Runner(
        app=app,
        artifact_service=artifact_service,
        session_service=session_service,
        credential_service=credential_service,
    )

    print("Welcome to Travel Planner CLI!")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("[You]: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        content = types.Content(role="user", parts=[types.Part(text=user_input)])
        agen = runner.run_async(
            user_id=session.user_id, session_id=session.id, new_message=content
        )

        async for event in agen:
            if event.content and event.content.parts:
                text = "".join(part.text for part in event.content.parts if part.text)
                if text:
                    print(f"[{event.author}]: {text}")

    await runner.close()


if __name__ == "__main__":
    asyncio.run(run_cli())
