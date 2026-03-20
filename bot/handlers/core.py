from typing import Dict, Any, Callable

def handle_start() -> str:
    return "Welcome! I am your LMS Helper Bot."

def handle_help() -> str:
    return "Commands:\n/start - welcome\n/help - command list\n/health - check status\n/scores - get scores"

def handle_health() -> str:
    # Later: call the backend health endpoint
    return "Status: OK (Placeholder)"

def handle_scores(args: str = "") -> str:
    return f"Scores for {args or 'all'}: (Placeholder)"

def handle_unknown(text: str) -> str:
    return f"I don't understand: {text}"

# Dispatcher for CLI mode
COMMANDS: Dict[str, Callable[..., str]] = {
    "/start": handle_start,
    "/help": handle_help,
    "/health": handle_health,
    "/scores": handle_scores,
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
