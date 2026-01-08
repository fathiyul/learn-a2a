# Core A2A types for defining agent capabilities
# For running the server
import uvicorn
from a2a.server.agent_execution.agent_executor import AgentExecutor

# Server framework components
from a2a.server.apps.jsonrpc.fastapi_app import A2AFastAPIApplication
from a2a.server.request_handlers.default_request_handler import DefaultRequestHandler
from a2a.server.tasks.inmemory_task_store import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

# Message utilities
from a2a.utils.message import new_agent_text_message

PORT = 8000

# Define the agent's skill using real SDK classes
echo_skill = AgentSkill(
    id="echo_messages",
    name="Echo Messages",
    description="Repeats whatever you say back to you.",
    tags=["echo", "simple", "demo"],
    examples=["Hello there!", "How are you doing?", "Echo this message back to me."],
    input_modes=["text/plain"],
    output_modes=["text/plain"],
)

# Define agent capabilities
capabilities = AgentCapabilities(
    streaming=False, push_notifications=False, state_transition_history=True
)

# Create the agent card using real SDK classes
agent_card = AgentCard(
    name="SDK Echo Agent",
    description="An echo agent built with the official A2A SDK to demonstrate best practices.",
    url=f"http://localhost:{PORT}",
    version="1.0.0",
    protocol_version="0.3.0",
    skills=[echo_skill],
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    capabilities=capabilities,
)


class EchoAgentExecutor(AgentExecutor):
    """
    Business logic implementation using the real A2A SDK AgentExecutor.
    The SDK handles all protocol complexity for us.
    """

    async def execute(self, context, event_queue):
        """
        Execute the echo logic using the SDK pattern.

        Args:
            context: RequestContext containing the user's input and metadata.
            event_queue: EventQueue for publishing response events.
        """
        try:
            # Get the user's input - this returns a string with all text parts combined
            user_text = context.get_user_input()

            # Handle the case where no text was found
            if not user_text or user_text.strip() == "":
                # Create an error message using the SDK utility
                error_message = new_agent_text_message(
                    "I didn't receive any text to echo. Please send me a message with text content."
                )
                await event_queue.enqueue_event(error_message)
                return

            # Create and enqueue the echo response using the SDK utility
            echo_message = new_agent_text_message(f"You said: '{user_text.strip()}'")
            await event_queue.enqueue_event(echo_message)

        except Exception as e:
            # The SDK provides structured error handling
            error_message = new_agent_text_message(
                f"Error processing your message: {str(e)}"
            )
            await event_queue.enqueue_event(error_message)

    async def cancel(self, task_id, event_queue):
        """
        Handle task cancellation using the SDK interface.

        Args:
            task_id: The ID of the task being canceled.
            event_queue: EventQueue for publishing cancellation events.
        """
        cancel_message = new_agent_text_message(
            f"Echo task {task_id} has been canceled."
        )
        await event_queue.enqueue_event(cancel_message)


def create_app():
    """Create and configure the A2A application using real SDK components."""

    # Create the agent executor
    executor = EchoAgentExecutor()

    # Create task store for managing task state
    task_store = InMemoryTaskStore()

    # Create the request handler that coordinates everything
    request_handler = DefaultRequestHandler(
        agent_executor=executor, task_store=task_store
    )

    # Create the A2A FastAPI application
    app = A2AFastAPIApplication(agent_card=agent_card, http_handler=request_handler)

    # Build and return the configured FastAPI app
    return app.build()


if __name__ == "__main__":
    print("🚀 Starting A2A SDK Echo Agent...")
    print(f"📡 Agent Card: http://localhost:{PORT}/.well-known/agent-card.json")
    print(f"🔗 A2A Endpoint: http://localhost:{PORT}/")

    app = create_app()

    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
