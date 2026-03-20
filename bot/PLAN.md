# LMS Helper Bot Development Plan

## Overview
The goal is to build a testable, maintainable Telegram bot that helps students interact with the LMS and query information using LLM.

## Task 1: Scaffold and Test Mode
- Establish a project structure with a clear separation between the Telegram transport layer and the business logic.
- Implement a `--test` CLI mode for the entry point `bot.py` to allow offline verification of command handlers.
- Use `uv` for dependency management and `pydantic-settings` for configuration.

## Task 2: Backend Integration
- Implement services to interact with the LMS API (e.g., fetching scores, checking health).
- Update handlers to use these services instead of returning placeholder text.
- Ensure all API calls are asynchronous to prevent blocking the bot.

## Task 3: LLM Intent Routing
- Integrate an LLM (e.g., Qwen-code API) to route natural language queries to the appropriate handlers or provide direct answers.
- Implement a fallback mechanism for unknown queries.

## Task 4: Deployment and Monitoring
- Containerize the bot using Docker and add it to `docker-compose.yml`.
- Set up logging and monitoring to ensure the bot is running reliably on the VM.
- Verify the bot's functionality in a real Telegram environment.

## Architecture
The bot follows a layered architecture:
- **Entry Point (`bot.py`)**: Handles CLI arguments and Telegram polling.
- **Handlers Layer (`handlers/`)**: Pure functions that process commands and return text responses.
- **Services Layer (`services/`)**: API clients for external systems (LMS, LLM).
- **Configuration (`config.py`)**: Centralized settings management.
