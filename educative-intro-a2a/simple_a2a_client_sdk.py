import uuid

import requests

PORT = 8000


def main():
    # Step 1: Discover the Agent
    base_url = f"http://localhost:{PORT}"
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
                "parts": [{"kind": "text", "text": "Hello A2A world!"}],
            }
        },
    }

    try:
        response = requests.post(base_url, json=message).json()
    except requests.RequestException as e:
        print(f"❌ Communication failed: {e}")
        return

    # Step 3: Handle the Response
    # The SDK returns Message directly, not Task with history like raw implementation
    if "result" in response:
        result = response["result"]
        if isinstance(result, dict) and "parts" in result:
            # This is a direct Message response from SDK
            agent_reply = result["parts"][0]["text"]
            print(f"🤖 Agent: {agent_reply}")
        else:
            # This might be a Task response (for compatibility)
            print(
                f"📋 Task Status: {result.get('status', {}).get('state', 'completed')}"
            )

            # Find agent's reply in history
            for msg in result.get("history", []):
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
