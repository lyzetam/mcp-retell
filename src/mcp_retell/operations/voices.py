"""Voice operations — list, get."""

from __future__ import annotations

from ..client import RetellClient


def list_voices(client: RetellClient) -> list[dict]:
    """List available voices from Retell's voice library (sync)."""
    voices = client.get_sync("/list-voices")
    if not isinstance(voices, list):
        voices = [voices]
    return [
        {
            "voice_id": v.get("voice_id"),
            "voice_name": v.get("voice_name"),
            "provider": v.get("provider"),
            "gender": v.get("gender"),
            "accent": v.get("accent"),
        }
        for v in voices
    ]


def get_voice(client: RetellClient, voice_id: str) -> dict:
    """Get details of a specific voice (sync)."""
    return client.get_sync(f"/get-voice/{voice_id}")
