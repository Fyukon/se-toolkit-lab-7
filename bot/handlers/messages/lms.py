def handle_health() -> str:
    # Later: call the backend health endpoint
    return "Status: OK (Placeholder)"

def handle_scores(args: str = "") -> str:
    return f"Scores for {args or 'all'}: (Placeholder)"
