"""Retell MCP Server — backward-compatible async @mcp.tool wrappers.

Tool names match the original server.py for drop-in replacement.
"""

from __future__ import annotations

import json
from typing import Optional

from mcp.server.fastmcp import FastMCP

from .client import RetellClient
from .operations import agents, calls, phones, voices

mcp = FastMCP("retell")

_client: RetellClient | None = None


def _get_client() -> RetellClient:
    global _client
    if _client is None:
        _client = RetellClient()
    return _client


# --- Agent Management ---

@mcp.tool()
async def list_agents() -> str:
    """List all voice agents."""
    c = _get_client()
    data = await c.get("/list-agents")
    if not isinstance(data, list):
        data = [data]
    result = [
        {
            "agent_id": a.get("agent_id"),
            "agent_name": a.get("agent_name"),
            "voice_id": a.get("voice_id"),
            "language": a.get("language"),
            "created_at": a.get("last_modification_timestamp"),
        }
        for a in data
    ]
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_agent(agent_id: str) -> str:
    """Get details of a specific agent."""
    c = _get_client()
    data = await c.get(f"/get-agent/{agent_id}")
    return json.dumps(data, indent=2)


@mcp.tool()
async def create_agent(
    agent_name: str,
    voice_id: str,
    prompt: str,
    language: str = "en-US",
    begin_message: Optional[str] = None,
    model: str = "gpt-4o-mini",
    responsiveness: float = 1.0,
    interruption_sensitivity: float = 1.0,
    enable_backchannel: bool = True,
) -> str:
    """Create a new voice agent."""
    c = _get_client()
    payload: dict = {
        "agent_name": agent_name,
        "voice_id": voice_id,
        "response_engine": {"type": "retell-llm", "llm_id": model},
        "llm_websocket_url": None,
        "voice_model": "eleven_turbo_v2",
        "language": language,
        "prompt": prompt,
        "responsiveness": responsiveness,
        "interruption_sensitivity": interruption_sensitivity,
        "enable_backchannel": enable_backchannel,
    }
    if begin_message:
        payload["begin_message"] = begin_message

    data = await c.post("/create-agent", json=payload)
    return json.dumps(data, indent=2)


@mcp.tool()
async def update_agent(
    agent_id: str,
    agent_name: Optional[str] = None,
    prompt: Optional[str] = None,
    begin_message: Optional[str] = None,
    voice_id: Optional[str] = None,
) -> str:
    """Update an existing agent."""
    c = _get_client()
    payload: dict = {}
    if agent_name:
        payload["agent_name"] = agent_name
    if prompt:
        payload["prompt"] = prompt
    if begin_message:
        payload["begin_message"] = begin_message
    if voice_id:
        payload["voice_id"] = voice_id

    data = await c.patch(f"/update-agent/{agent_id}", json=payload)
    return json.dumps(data, indent=2)


@mcp.tool()
async def delete_agent(agent_id: str) -> str:
    """Delete an agent."""
    c = _get_client()
    await c.delete(f"/delete-agent/{agent_id}")
    return json.dumps({"status": "deleted", "agent_id": agent_id}, indent=2)


# --- Call Management ---

@mcp.tool()
async def create_phone_call(
    agent_id: str,
    to_number: str,
    from_number: str,
    metadata: Optional[str] = None,
) -> str:
    """Initiate an outbound phone call."""
    c = _get_client()
    payload: dict = {
        "agent_id": agent_id,
        "to_number": to_number,
        "from_number": from_number,
    }
    if metadata:
        payload["metadata"] = json.loads(metadata)

    data = await c.post("/create-phone-call", json=payload)
    return json.dumps(data, indent=2)


@mcp.tool()
async def list_calls(
    agent_id: Optional[str] = None,
    limit: int = 50,
    sort_order: str = "descending",
) -> str:
    """List phone calls."""
    c = _get_client()
    params: dict = {"limit": limit, "sort_order": sort_order}
    if agent_id:
        params["filter_criteria"] = json.dumps([{
            "member": "agent_id", "operator": "eq", "value": agent_id,
        }])

    data = await c.get("/list-calls", params=params)
    if not isinstance(data, list):
        data = [data]
    result = [
        {
            "call_id": call.get("call_id"),
            "agent_id": call.get("agent_id"),
            "call_type": call.get("call_type"),
            "call_status": call.get("call_status"),
            "from_number": call.get("from_number"),
            "to_number": call.get("to_number"),
            "start_timestamp": call.get("start_timestamp"),
            "end_timestamp": call.get("end_timestamp"),
            "duration_ms": (call.get("end_timestamp", 0) - call.get("start_timestamp", 0))
            if call.get("end_timestamp") else None,
            "disconnection_reason": call.get("disconnection_reason"),
        }
        for call in data
    ]
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_call(call_id: str) -> str:
    """Get details of a specific call."""
    c = _get_client()
    data = await c.get(f"/get-call/{call_id}")
    return json.dumps(data, indent=2)


@mcp.tool()
async def get_call_transcript(call_id: str) -> str:
    """Get the transcript of a call."""
    c = _get_client()
    call_data = await c.get(f"/get-call/{call_id}")
    return json.dumps({
        "call_id": call_id,
        "transcript": call_data.get("transcript", ""),
        "call_analysis": call_data.get("call_analysis"),
        "duration_ms": (call_data.get("end_timestamp", 0) - call_data.get("start_timestamp", 0))
        if call_data.get("end_timestamp") else None,
    }, indent=2)


# --- Phone Numbers ---

@mcp.tool()
async def list_phone_numbers() -> str:
    """List all registered phone numbers."""
    c = _get_client()
    data = await c.get("/list-phone-numbers")
    if not isinstance(data, list):
        data = [data]
    result = [
        {
            "phone_number": n.get("phone_number"),
            "phone_number_pretty": n.get("phone_number_pretty"),
            "inbound_agent_id": n.get("inbound_agent_id"),
            "area_code": n.get("area_code"),
            "nickname": n.get("nickname"),
        }
        for n in data
    ]
    return json.dumps(result, indent=2)


@mcp.tool()
async def update_phone_number(
    phone_number: str,
    inbound_agent_id: Optional[str] = None,
    nickname: Optional[str] = None,
) -> str:
    """Update a phone number configuration."""
    c = _get_client()
    payload: dict = {}
    if inbound_agent_id:
        payload["inbound_agent_id"] = inbound_agent_id
    if nickname:
        payload["nickname"] = nickname

    data = await c.patch(f"/update-phone-number/{phone_number}", json=payload)
    return json.dumps(data, indent=2)


# --- Voices ---

@mcp.tool()
async def list_voices() -> str:
    """List available voices from Retell's voice library."""
    c = _get_client()
    data = await c.get("/list-voices")
    if not isinstance(data, list):
        data = [data]
    result = [
        {
            "voice_id": v.get("voice_id"),
            "voice_name": v.get("voice_name"),
            "provider": v.get("provider"),
            "gender": v.get("gender"),
            "accent": v.get("accent"),
        }
        for v in data
    ]
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_voice(voice_id: str) -> str:
    """Get details of a specific voice."""
    c = _get_client()
    data = await c.get(f"/get-voice/{voice_id}")
    return json.dumps(data, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
