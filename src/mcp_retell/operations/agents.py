"""Agent operations — list, get, create, update, delete."""

from __future__ import annotations

from typing import Optional

from ..client import RetellClient


def list_agents(client: RetellClient) -> list[dict]:
    """List all voice agents (sync)."""
    agents = client.get_sync("/list-agents")
    if not isinstance(agents, list):
        agents = [agents]
    return [
        {
            "agent_id": a.get("agent_id"),
            "agent_name": a.get("agent_name"),
            "voice_id": a.get("voice_id"),
            "language": a.get("language"),
            "created_at": a.get("last_modification_timestamp"),
        }
        for a in agents
    ]


def get_agent(client: RetellClient, agent_id: str) -> dict:
    """Get details of a specific agent (sync)."""
    return client.get_sync(f"/get-agent/{agent_id}")


def create_agent(
    client: RetellClient,
    agent_name: str,
    voice_id: str,
    prompt: str,
    language: str = "en-US",
    begin_message: Optional[str] = None,
    model: str = "gpt-4o-mini",
    responsiveness: float = 1.0,
    interruption_sensitivity: float = 1.0,
    enable_backchannel: bool = True,
) -> dict:
    """Create a new voice agent (sync)."""
    payload: dict = {
        "agent_name": agent_name,
        "voice_id": voice_id,
        "response_engine": {
            "type": "retell-llm",
            "llm_id": model,
        },
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

    return client.post_sync("/create-agent", json=payload)


def update_agent(
    client: RetellClient,
    agent_id: str,
    agent_name: Optional[str] = None,
    prompt: Optional[str] = None,
    begin_message: Optional[str] = None,
    voice_id: Optional[str] = None,
) -> dict:
    """Update an existing agent (sync)."""
    payload: dict = {}
    if agent_name:
        payload["agent_name"] = agent_name
    if prompt:
        payload["prompt"] = prompt
    if begin_message:
        payload["begin_message"] = begin_message
    if voice_id:
        payload["voice_id"] = voice_id

    return client.patch_sync(f"/update-agent/{agent_id}", json=payload)


def delete_agent(client: RetellClient, agent_id: str) -> dict:
    """Delete an agent (sync)."""
    client.delete_sync(f"/delete-agent/{agent_id}")
    return {"status": "deleted", "agent_id": agent_id}
