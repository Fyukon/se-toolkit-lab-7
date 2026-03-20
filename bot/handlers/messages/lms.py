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
        lab_id = item.get("lab_id")
        lab_name = item.get("lab_name")
        if lab_id and lab_name:
            labs[lab_id] = lab_name
            
    if not labs:
        return "No labs available at the moment."
    
    output = "Available labs:\n"
    for lid, name in sorted(labs.items()):
        output += f"- {lid.replace('-', ' ').title()} — {name}\n"
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
        task_name = entry.get("task_name", "Unknown Task")
        pass_rate = entry.get("pass_rate", 0) * 100
        attempts = entry.get("attempts", 0)
        output += f"- {task_name}: {pass_rate:.1f}% ({attempts} attempts)\n"
    return output
