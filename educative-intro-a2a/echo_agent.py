import uuid
from datetime import datetime
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Part(BaseModel):
    kind: str
    text: str = None


class Message(BaseModel):
    kind: str = "message"
    messageId: str
    role: str
    parts: List[Part]


class MessageParams(BaseModel):
    message: Message


class JSONRPCRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: str
    method: str
    params: MessageParams


# NEW: Add this endpoint for A2A discovery
@app.get("/.well-known/agent-card.json")
def agent_card():
    """A2A Agent Discovery Endpoint"""
    return {
        "name": "Echo Agent",
        "description": "A simple agent that echoes your messages back",
        "url": "http://localhost:8000",
        "version": "1.0.0",
        "protocolVersion": "0.3.0",
        "skills": [
            {
                "id": "echo",
                "name": "Echo Messages",
                "description": "Repeats whatever you say",
                "examples": ["Hello", "How are you?"],
            }
        ],
        "capabilities": {"streaming": False},
        "defaultInputModes": ["text/plain"],
        "defaultOutputModes": ["text/plain"],
    }


@app.get("/")
def hello():
    return {"message": "Hello from our A2A agent!"}


@app.post("/")
def handle_message(request: JSONRPCRequest):
    """A2A Message Handler"""
    # Validate the method
    if request.method != "message/send":
        return {
            "jsonrpc": "2.0",
            "id": request.id,
            "error": {"code": -32601, "message": "Method not found"},
        }

    # Extract the user's message
    user_message = request.params.message
    user_text = user_message.parts[0].text if user_message.parts else "No text"

    # Create our A2A response as a completed task
    task = {
        "kind": "task",
        "id": str(uuid.uuid4()),
        "contextId": str(uuid.uuid4()),
        "status": {
            "state": "completed",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        },
        "history": [
            # Include the original user message
            user_message.dict(),
            # Add our agent response
            {
                "kind": "message",
                "messageId": str(uuid.uuid4()),
                "role": "agent",
                "parts": [{"kind": "text", "text": f"You said: '{user_text}'"}],
            },
        ],
    }

    return {"jsonrpc": "2.0", "id": request.id, "result": task}


if __name__ == "__main__":
    import uvicorn

    PORT = 8000

    print(f"🚀 Starting basic web server on http://localhost:{PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
