async def handle_start() -> str:
    return "Welcome! I am your LMS Helper Bot."

async def handle_help() -> str:
    return (
        "Available commands:\n"
        "/start — welcome message\n"
        "/help — list all available commands\n"
        "/health — check backend status\n"
        "/labs — list available labs\n"
        "/scores <lab> — per-task pass rates for a specific lab\n"
        "/version — show bot version"
    )
