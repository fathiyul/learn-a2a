# Intro to A2A

[Educative Course](https://www.educative.io/courses/agent2agent-protocol)

## Key concepts

- agent discovery
- request handling
- authorization
- and error management to build interoperable agent systems

**Why?**

Many agents by different teams: python, js, langgraph, crewai, no shared rules on how to communicate with each other

A2A: a structured intent schema **protocol** that standardizes how agents:
- introduce themselves (capabilities)
- ask for work (requests)
- share progress (streaming)
- fail safely (errors)
- prove permissions (authorization)

**Installation**

```
uv add a2a-sdk
```
you can add extensions such as:
```
uv add "a2a-sdk[all]"        # All features
uv add "a2a-sdk[http-server]"  # HTTP Server
uv add "a2a-sdk[grpc]"         # gRPC Support
uv add "a2a-sdk[telemetry]"    # OpenTelemetry Tracing
uv add "a2a-sdk[encryption]"   # Encryption
```
MCP: tool use

A2A: inter-agent protocol

Under Linux Foundation

**Agent Cards** = metadata + list of skills

**skill** = specific capability / function. defined using `a2a.types.AgentSkill`, example:

```
skill = AgentSkill(
    id='helloWorld',
    name='Returns hello world',
    description='Just returns hello world',
    tags=['hello world'],
    examples=['hi', 'hello world'],
 )
```

Agent card: JSON file typically stored in `.well-known/agent-card.json`. An example:

```
public_agent_card = AgentCard(
    name='Hello World Agent',
    description='Just a hello world agent',
    url='http://localhost:9999/',
    version='1.0.0',
    protocolVersion='0.3.0',
    defaultInputModes=['text/plain'],
    defaultOutputModes=['text/plain'],
    capabilities=AgentCapabilities(streaming=True),
    skills=[skill],
    supportsAuthenticatedExtendedCard=True,
  )
```
Agents communicates thru 3 constructs:
- Messages: text, file, data. stateless
- Tasks: long work. streaming updates
- Artifacts: final structured output from task

*messages* are how agents talk, *tasks* are how they work, and *artifacts* are what they produce - the durable outputs that persist after the conversation ends.

# Build A2A Client and Server

Using FastAPI

## Server

1. make standard fastapi server
2. add `@app.get("/.well-known/agent-card.json")` to make it A2A compliant.

Example response:
```
{
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
      "examples": [
        "Hello",
        "How are you?"
      ]
    }
  ],
  "capabilities": {
    "streaming": false
  },
  "defaultInputModes": [
    "text/plain"
  ],
  "defaultOutputModes": [
    "text/plain"
  ]
}
```
3. Add message structure validation: using Pydantic to build a POST request validation schema.

Example Pydantic objects:
```
from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime

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
```
Minimal (without actual agent logic implementation):
```
@app.post("/")
def handle_message(request: JSONRPCRequest):
    """A2A Message Handler - Coming Next!"""
    return {"jsonrpc": "2.0", "id": request.id, "result": "Handler coming soon!"}
```
With logic implementation:
```
@app.post("/")
def handle_message(request: JSONRPCRequest):
    """A2A Message Handler"""
    # Validate the method
    if request.method != "message/send":
        return {
            "jsonrpc": "2.0", 
            "id": request.id, 
            "error": {
                "code": -32601, 
                "message": "Method not found"
            }
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
            "timestamp": datetime.utcnow().isoformat() + "Z"
        },
        "history": [
            # Include the original user message
            user_message.dict(),
            # Add our agent response
            {
                "kind": "message",
                "messageId": str(uuid.uuid4()),
                "role": "agent",
                "parts": [{"kind": "text", "text": f"You said: '{user_text}'"}]
            }
        ]
    }
    
    return {"jsonrpc": "2.0", "id": request.id, "result": task}
```
Full code is in `echo_agent.py`

## Client

`simple_a2a_client.py`

```
import requests
import uuid
import json

def main():
    # Step 1: Discover the Agent
    base_url = "http://localhost:8000"
    print("🔍 Discovering A2A agent...")
    
    try:
        agent_card = requests.get(f"{base_url}/.well-known/agent-card.json").json()
        print(f"✅ Found: {agent_card['name']} - {agent_card['description']}")
    except requests.RequestException as e:
        print(f"❌ Discovery failed: {e}")
        return
    
    # Step 2: Send a Message using A2A JSON-RPC
    print("\n💬 Sending message...")
    
    message = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "message/send",
        "params": {
            "message": {
                "kind": "message",
                "messageId": str(uuid.uuid4()),
                "role": "user",
                "parts": [{"kind": "text", "text": "Hello A2A world!"}]
            }
        }
    }
    
    try:
        response = requests.post(base_url, json=message).json()
    except requests.RequestException as e:
        print(f"❌ Communication failed: {e}")
        return
    
    # Step 3: Handle the Response
    if "result" in response:
        task = response["result"] 
        print(f"📋 Task Status: {task['status']['state']}")
        
        # Find agent's reply in history
        for msg in task.get("history", []):
            if msg.get("role") == "agent":
                agent_reply = msg["parts"][0]["text"]
                print(f"🤖 Agent: {agent_reply}")
                break
    else:
        error = response.get("error", {})
        print(f"❌ Error: {error.get('message', 'Unknown error')}")
    
    print("\n✨ A2A communication complete!")

if __name__ == "__main__":
    main()
```

Now you can try it.

Personal comment:

- managing this manually will be a tedious task. need a wrapper around this

# Using A2A SDK

## Server
1. Define `AgentSkill`, `AgentCapabilities`, and `AgentCard`
2. For core functionalities, use `AgentExecutor` interface
3. Create App (`A2AFastAPIApplication`): wire everything together using the actual A2A SDK classes (like `InMemoryTaskStore`, `DefaultRequestHandler`).

See `sdk_echo_agent.py`

## Client

See `simple_a2a_client_sdk.py` for SDK-compatible client.

tl;dr, using SDK = a matter of extending `AgentExecutor`
