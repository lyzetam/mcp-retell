"""Phone number operations — list, update."""

from __future__ import annotations

from typing import Optional

from ..client import RetellClient


def list_phone_numbers(client: RetellClient) -> list[dict]:
    """List all registered phone numbers (sync)."""
    numbers = client.get_sync("/list-phone-numbers")
    if not isinstance(numbers, list):
        numbers = [numbers]
    return [
        {
            "phone_number": n.get("phone_number"),
            "phone_number_pretty": n.get("phone_number_pretty"),
            "inbound_agent_id": n.get("inbound_agent_id"),
            "area_code": n.get("area_code"),
            "nickname": n.get("nickname"),
        }
        for n in numbers
    ]


def update_phone_number(
    client: RetellClient,
    phone_number: str,
    inbound_agent_id: Optional[str] = None,
    nickname: Optional[str] = None,
) -> dict:
    """Update a phone number configuration (sync)."""
    payload: dict = {}
    if inbound_agent_id:
        payload["inbound_agent_id"] = inbound_agent_id
    if nickname:
        payload["nickname"] = nickname

    return client.patch_sync(f"/update-phone-number/{phone_number}", json=payload)
