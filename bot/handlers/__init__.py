from typing import Dict, Any, Callable, Coroutine
from .messages.core import handle_start, handle_help
from .messages.lms import handle_health, handle_scores, handle_labs
from .messages.info import handle_version
from services.llm import route_intent

def handle_unknown_text(text: str) -> str:
    """Fallback for non-slash commands that should be routed to LLM."""
    return f"Let me think about: {text}..."

# Dispatcher for CLI mode
COMMANDS: Dict[str, Callable[..., Coroutine[Any, Any, str]]] = {
    "/start": handle_start,
    "/help": handle_help,
    "/health": handle_health,
    "/labs": handle_labs,
    "/scores": handle_scores,
    "/version": handle_version,
}

async def dispatch_command(text: str) -> str:
    parts = text.split()
    if not parts:
        return ""
    
    command = parts[0].lower()
    args = " ".join(parts[1:])
    
    if command.startswith("/"):
        handler = COMMANDS.get(command)
        if handler:
            try:
                if args:
                     return await handler(args)
                return await handler()
            except TypeError:
                return await handler()
        return f"Unknown command: {command}. Use /help to see available commands."
    
    # If not a command, route to LLM
    return await route_intent(text)
