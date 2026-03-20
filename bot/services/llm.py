import json
import sys
import httpx
from config import settings
from services.lms_api import lms_client
from typing import List, Dict, Any

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_items",
            "description": "Get a list of all labs and tasks in the course",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_learners",
            "description": "Get a list of enrolled students and their groups",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_scores",
            "description": "Get score distribution (4 buckets) for a specific lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab ID, e.g., 'lab-01'"}
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pass_rates",
            "description": "Get per-task average scores and attempt counts for a specific lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab ID, e.g., 'lab-01'"}
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_timeline",
            "description": "Get submissions timeline (submissions per day) for a specific lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab ID, e.g., 'lab-01'"}
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_groups",
            "description": "Get per-group performance (scores and student counts) for a specific lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab ID, e.g., 'lab-01'"}
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_learners",
            "description": "Get the top N students by score for a specific lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab ID, e.g., 'lab-01'"},
                    "limit": {"type": "integer", "description": "Number of students, default 5"}
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_completion_rate",
            "description": "Get the completion rate percentage for a specific lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab ID, e.g., 'lab-01'"}
                },
                "required": ["lab"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "trigger_sync",
            "description": "Refresh data from the autochecker by triggering the ETL pipeline",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]

async def execute_tool(name: str, args: Dict[str, Any]) -> str:
    """Dispatches tool calls to the LMS API client."""
    print(f"[tool] LLM called: {name}({args})", file=sys.stderr)
    
    method = getattr(lms_client, name, None)
    if not method:
        return f"Error: Tool {name} not found."
    
    result = await method(**args)
    
    if result["status"] == "ok":
        data = result["data"]
        # Basic summary for stderr
        summary = f"{len(data)} items" if isinstance(data, list) else "1 item"
        print(f"[tool] Result: {summary}", file=sys.stderr)
        return json.dumps(data)
    
    print(f"[tool] Error: {result['message']}", file=sys.stderr)
    return f"Error from API: {result['message']}"

async def route_intent(user_message: str) -> str:
    """Sends message to LLM, handles tool calls, and returns final summary."""
    if not settings.LLM_API_KEY:
        return "LLM_API_KEY is not configured. I can only handle /slash commands."

    messages = [
        {"role": "system", "content": "You are a helpful assistant for an LMS course. Use the provided tools to fetch data and answer student questions accurately. If multiple steps are needed, do them. If you cannot answer with tools, explain what you can do."},
        {"role": "user", "content": user_message}
    ]

    async with httpx.AsyncClient(timeout=60.0) as client:
        for _ in range(5):  # Max 5 tool iterations
            payload = {
                "model": settings.LLM_API_MODEL,
                "messages": messages,
                "tools": TOOLS,
                "tool_choice": "auto"
            }
            
            response = await client.post(
                f"{settings.LLM_API_BASE_URL.rstrip('/')}/v1/chat/completions",
                headers={"Authorization": f"Bearer {settings.LLM_API_KEY}"},
                json=payload
            )
            
            if response.status_code != 200:
                return f"LLM error: HTTP {response.status_code} - {response.text}"
            
            res_data = response.json()
            choice = res_data["choices"][0]
            msg = choice["message"]
            
            if not msg.get("tool_calls"):
                return msg["content"]
            
            # Process tool calls
            messages.append(msg)
            tool_calls = msg["tool_calls"]
            print(f"[summary] Feeding {len(tool_calls)} tool results back to LLM", file=sys.stderr)
            
            for tool_call in tool_calls:
                name = tool_call["function"]["name"]
                args = json.loads(tool_call["function"]["arguments"])
                result = await execute_tool(name, args)
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "name": name,
                    "content": result
                })
        
        return "I'm sorry, the conversation became too complex. Please try a simpler question."
