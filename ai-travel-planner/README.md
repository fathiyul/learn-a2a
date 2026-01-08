# AI Travel Planner

[Educative Project](https://www.educative.io/projects/build-an-ai-travel-planner-with-multi-agent-a2a-protocol)

An AI-powered travel planning agent built using the Agent-to-Agent (A2A) protocol. This intelligent assistant helps you plan trips by coordinating multiple specialized agents to find flights, hotels, attractions, and weather information.

## Features

- **Multi-Agent Architecture**: Coordinated team of specialized agents working together
- **Flight Search**: Find flights between cities with date filtering
- **Hotel Recommendations**: Discover hotels based on location, rating, and price
- **Weather Forecasts**: Get weather information for your destination
- **Attraction Suggestions**: Find popular tourist attractions and activities
- **Natural Language Interface**: Plan trips using conversational commands

## Architecture

The system consists of multiple specialized agents:

- **Root Agent**: Orchestrates the travel planning process
- **Flight Agent**: Queries flight database for available flights
- **Hotel Agent**: Finds hotels based on your preferences
- **Weather Agent**: Provides weather forecasts (remote agent)
- **Attractions Agent**: Suggests activities and sights

## Prerequisites

- Python 3.13 or higher
- uv (Python package manager)

## Installation

1. Clone the repository and navigate to the project:
```bash
cd ai-travel-planner
```

2. Create a `.env` file from the example:
```bash
cp .env.example .env
```

3. Fill in the required environment variables in `.env`.

## Usage

### Start the CLI Interface

```bash
uv run cli.py
```

### Start the A2A Server (Optional)

To run as an A2A-compliant server:

```bash
uv run adk api_server --a2a --port 8001 --host 0.0.0.0 agents
```

## Example Queries

Try these natural language commands:

- "Plan me a 3-day trip to Paris."
- "What hotels are available in Rome under $100?"
- "Show me flights from New York to London on October 10."
- "What will the weather be like in Paris next week?"
- "Plan me a trip going from New York to London starting from 01-01 and then returning on 01-04."

## How It Works

1. The root agent receives your travel request
2. It breaks down the request and delegates tasks to specialized sub-agents
3. Each agent uses its tools and knowledge to gather information
4. The root agent consolidates all information into a coherent travel plan
5. You can refine the plan with follow-up questions

## Exiting the CLI

Type `exit` or `quit` to close the CLI session.

## Technical Details

- Built with Google's A2A SDK and ADK
- Uses Gemini 2.5 Flash for natural language understanding
- Implements the A2A protocol for agent interoperability
- Mock datasets for flights and hotels included for demonstration
