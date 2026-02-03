"""Call operations — create, list, get, get transcript."""

from __future__ import annotations

import json
from typing import Optional

from ..client import RetellClient


def create_phone_call(
    client: RetellClient,
    agent_id: str,
    to_number: str,
    from_number: str,
    metadata: Optional[str] = None,
) -> dict:
    """Initiate an outbound phone call (sync)."""
    payload: dict = {
        "agent_id": agent_id,
        "to_number": to_number,
        "from_number": from_number,
    }
    if metadata:
        payload["metadata"] = json.loads(metadata)

    return client.post_sync("/create-phone-call", json=payload)


def list_calls(
    client: RetellClient,
    agent_id: Optional[str] = None,
    limit: int = 50,
    sort_order: str = "descending",
) -> list[dict]:
    """List phone calls (sync)."""
    params: dict = {"limit": limit, "sort_order": sort_order}
    if agent_id:
        params["filter_criteria"] = json.dumps([{
            "member": "agent_id",
            "operator": "eq",
            "value": agent_id,
        }])

    calls = client.get_sync("/list-calls", params=params)
    if not isinstance(calls, list):
        calls = [calls]
    return [
        {
            "call_id": c.get("call_id"),
            "agent_id": c.get("agent_id"),
            "call_type": c.get("call_type"),
            "call_status": c.get("call_status"),
            "from_number": c.get("from_number"),
            "to_number": c.get("to_number"),
            "start_timestamp": c.get("start_timestamp"),
            "end_timestamp": c.get("end_timestamp"),
            "duration_ms": (c.get("end_timestamp", 0) - c.get("start_timestamp", 0))
            if c.get("end_timestamp") else None,
            "disconnection_reason": c.get("disconnection_reason"),
        }
        for c in calls
    ]


def get_call(client: RetellClient, call_id: str) -> dict:
    """Get details of a specific call (sync)."""
    return client.get_sync(f"/get-call/{call_id}")


def get_call_transcript(client: RetellClient, call_id: str) -> dict:
    """Get the transcript of a call (sync)."""
    call_data = client.get_sync(f"/get-call/{call_id}")
    return {
        "call_id": call_id,
        "transcript": call_data.get("transcript", ""),
        "call_analysis": call_data.get("call_analysis"),
        "duration_ms": (call_data.get("end_timestamp", 0) - call_data.get("start_timestamp", 0))
        if call_data.get("end_timestamp") else None,
    }
