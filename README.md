# Learn A2A Protocol

A comprehensive collection of learning materials and practical examples for the [Agent-to-Agent (A2A) protocol](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/).

## Overview

The A2A protocol enables different AI agents to communicate and collaborate seamlessly, creating more powerful and flexible multi-agent systems. This repository provides hands-on examples ranging from basic implementations to production-ready applications.

## Getting Started

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager

### Installation

```bash
uv sync
```

## Examples

### AI Travel Planner

A practical multi-agent application that demonstrates real-world A2A protocol usage.

**Location**: `ai-travel-planner/`

An intelligent travel planning assistant that coordinates multiple specialized agents to help users plan trips:

- **Flight Agent**: Searches and filters flight options
- **Hotel Agent**: Finds accommodations based on preferences
- **Weather Agent**: Provides destination weather forecasts
- **Attractions Agent**: Recommends local activities and sights

For detailed setup and usage, see [ai-travel-planner/README.md](ai-travel-planner/README.md).

### Basic A2A Examples

Fundamental examples demonstrating A2A protocol implementation patterns.

**Location**: `educative-intro-a2a/`

- **echo_agent.py**: Minimal A2A agent using raw FastAPI
- **sdk_echo_agent.py**: Production-ready agent using the official SDK
- **simple_a2a_client.py**: Basic client for raw implementation
- **simple_a2a_client_sdk.py**: Client for SDK-based agents

See [educative-intro-a2a/README.md](educative-intro-a2a/README.md) for detailed instructions.

## Project Structure

```
learn-a2a/
├── ai-travel-planner/          # Production-ready travel planning example
│   ├── agent.py               # Multi-agent definitions
│   ├── cli.py                 # Interactive CLI interface
│   ├── agents/                # Remote agent configurations
│   └── README.md              # Detailed documentation
├── educative-intro-a2a/       # Basic A2A protocol examples
│   ├── echo_agent.py
│   ├── sdk_echo_agent.py
│   ├── simple_a2a_client.py
│   ├── simple_a2a_client_sdk.py
│   └── README.md
└── pyproject.toml             # Project dependencies
```

## Key Concepts

- **Agent Discovery**: How agents find and connect to each other
- **Agent Cards**: Structured metadata describing agent capabilities
- **Message Protocols**: Standardized communication formats
- **Tool Integration**: Extending agents with external tools and APIs
- **Multi-Agent Orchestration**: Coordinating multiple agents to solve complex tasks

## Resources

- [A2A Protocol Official Blog](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
- [A2A SDK Documentation](https://github.com/google/a2a-sdk)
- [Google ADK Documentation](https://github.com/google/adk)

## License

See project root for license information.
