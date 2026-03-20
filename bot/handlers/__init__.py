from typing import Dict, Any, Callable, Coroutine
from .messages.core import handle_start, handle_help
from .messages.lms import handle_health, handle_scores, handle_labs
from .messages.info import handle_version

def handle_unknown(text: str) -> str:
    return f"I don't understand: {text}. Use /help to see available commands."

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
    
    handler = COMMANDS.get(command)
    if handler:
        try:
            if args:
                 return await handler(args)
            return await handler()
        except TypeError:
            # If handler doesn't accept args, call without them
            return await handler()
    
    return handle_unknown(text)
