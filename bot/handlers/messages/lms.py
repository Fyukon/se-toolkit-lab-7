from services.lms_api import lms_client

async def handle_health() -> str:
    """Checks the status of the backend service."""
    response = await lms_client.get_items()
    
    if response["status"] == "ok":
        items = response["data"]
        return f"Backend is healthy. {len(items)} items available."
    
    return f"Backend error: {response['message']}"

async def handle_labs() -> str:
    """Lists all available labs by filtering unique lab IDs from the items endpoint."""
    response = await lms_client.get_items()
    
    if response["status"] == "error":
        return f"Backend error: {response['message']}"
    
    items = response.get("data", [])
    labs = {}
    for item in items:
        # Check for lab type or just collect all with titles
        if item.get("type") == "lab":
            # Extract a lab-XX ID from title or use title as is
            title = item.get("title", "Unknown Lab")
            # We want keys like "lab-01", "lab-02" for /scores command
            import re
            match = re.search(r"Lab\s*(\d+)", title, re.IGNORECASE)
            lab_id = f"lab-{match.group(1)}" if match else f"lab-{item.get('id', '??')}"
            labs[lab_id] = title
            
    if not labs:
        return "No labs available at the moment."
    
    output = "Available labs:\n"
    for lid, name in sorted(labs.items()):
        output += f"- `{lid}` — {name}\n"
    return output

async def handle_scores(args: str = "") -> str:
    """Fetches task pass rates for a specific lab."""
    if not args:
        return "Error: Please specify a lab ID (e.g., /scores lab-04)."
    
    lab_id = args.strip().lower()
    response = await lms_client.get_pass_rates(lab_id)
    
    if response["status"] == "error":
        return f"Backend error: {response['message']}"
    
    data = response.get("data", [])
    if not data:
        return f"No data found for lab '{lab_id}'. Make sure it's correct."
    
    output = f"Pass rates for {lab_id.replace('-', ' ').title()}:\n"
    for entry in data:
        task_name = entry.get("task", "Unknown Task")
        # avg_score is already in 0-100 format based on curl output (88.8)
        pass_rate = entry.get("avg_score", 0)
        attempts = entry.get("attempts", 0)
        output += f"- {task_name}: {pass_rate:.1f}% ({attempts} attempts)\n"
    return output
