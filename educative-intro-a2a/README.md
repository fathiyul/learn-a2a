# Educative Intro to A2A

This repository contains examples demonstrating the Agent-to-Agent (A2A) protocol implementation using both raw FastAPI and the official A2A SDK.

## Usage

### Option 1: Basic FastAPI Implementation

**Server:**
```bash
uv run echo_agent.py
```
Server runs on `http://localhost:8000`

**Client:**
```bash
uv run simple_a2a_client.py
```

### Option 2: A2A SDK Implementation

**Server:**
```bash
uv run sdk_echo_agent.py
```
Server runs on `http://localhost:8000`

**Client:**
```bash
uv run simple_a2a_client_sdk.py
```

## What These Examples Do

- **echo_agent.py**: Minimal A2A agent that echoes back messages using raw FastAPI and Pydantic
- **sdk_echo_agent.py**: Production-ready A2A agent using the official SDK
- **simple_a2a_client.py**: Basic client to test the raw implementation
- **simple_a2a_client_sdk.py**: Client compatible with SDK-based agent

## Learning Resources

It's the implementation of the "[Introduction to Google’s Agent2Agent (A2A) Protocol](https://www.educative.io/courses/agent2agent-protocol)" course by Educative.io

See [NOTES.md](NOTES.md) for the learning notes.
