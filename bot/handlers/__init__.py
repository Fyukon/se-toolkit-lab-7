from typing import Dict, Any, Callable
from .messages.core import handle_start, handle_help
from .messages.lms import handle_health, handle_scores
from .messages.info import handle_version

def handle_unknown(text: str) -> str:
    return f"I don't understand: {text}"

# Dispatcher for CLI mode
COMMANDS: Dict[str, Callable[..., str]] = {
    "/start": handle_start,
    "/help": handle_help,
    "/health": handle_health,
    "/scores": handle_scores,
    "/version": handle_version,
}

def dispatch_command(text: str) -> str:
    parts = text.split()
    if not parts:
        return ""
    
    command = parts[0].lower()
    args = " ".join(parts[1:])
    
    handler = COMMANDS.get(command)
    if handler:
        if args:
            try:
                return handler(args)
            except TypeError:
                 return handler()
        return handler()
    
    return handle_unknown(text)
