"""Tests for Retell operations using respx mocks."""

import httpx
import respx

from mcp_retell.client import RetellClient
from mcp_retell.operations import agents, calls, phones, voices

BASE = "https://api.retellai.com"


def _client():
    return RetellClient(api_key="test-key", base_url=BASE)


# =============================================================================
# Agent operations
# =============================================================================


@respx.mock
def test_list_agents():
    respx.get(f"{BASE}/list-agents").mock(
        return_value=httpx.Response(200, json=[
            {"agent_id": "ag1", "agent_name": "Sales Bot", "voice_id": "v1", "language": "en-US", "last_modification_timestamp": 1700000000}
        ])
    )
    result = agents.list_agents(_client())
    assert len(result) == 1
    assert result[0]["agent_id"] == "ag1"
    assert result[0]["agent_name"] == "Sales Bot"


@respx.mock
def test_get_agent():
    respx.get(f"{BASE}/get-agent/ag1").mock(
        return_value=httpx.Response(200, json={"agent_id": "ag1", "agent_name": "Sales Bot", "prompt": "You are a sales agent."})
    )
    result = agents.get_agent(_client(), "ag1")
    assert result["agent_id"] == "ag1"
    assert result["prompt"] == "You are a sales agent."


@respx.mock
def test_create_agent():
    respx.post(f"{BASE}/create-agent").mock(
        return_value=httpx.Response(200, json={"agent_id": "ag2", "agent_name": "New Bot"})
    )
    result = agents.create_agent(_client(), "New Bot", "v1", "You are helpful.")
    assert result["agent_id"] == "ag2"


@respx.mock
def test_create_agent_with_options():
    respx.post(f"{BASE}/create-agent").mock(
        return_value=httpx.Response(200, json={"agent_id": "ag3", "agent_name": "Custom Bot"})
    )
    result = agents.create_agent(
        _client(), "Custom Bot", "v2", "Be helpful.",
        language="es-ES", begin_message="Hola!", model="gpt-4o",
        responsiveness=1.5, interruption_sensitivity=0.5, enable_backchannel=False,
    )
    assert result["agent_id"] == "ag3"


@respx.mock
def test_update_agent():
    respx.patch(f"{BASE}/update-agent/ag1").mock(
        return_value=httpx.Response(200, json={"agent_id": "ag1", "agent_name": "Updated Bot"})
    )
    result = agents.update_agent(_client(), "ag1", agent_name="Updated Bot")
    assert result["agent_name"] == "Updated Bot"


@respx.mock
def test_delete_agent():
    respx.delete(f"{BASE}/delete-agent/ag1").mock(
        return_value=httpx.Response(200, json={})
    )
    result = agents.delete_agent(_client(), "ag1")
    assert result["status"] == "deleted"
    assert result["agent_id"] == "ag1"


# =============================================================================
# Call operations
# =============================================================================


@respx.mock
def test_create_phone_call():
    respx.post(f"{BASE}/create-phone-call").mock(
        return_value=httpx.Response(200, json={"call_id": "call1", "agent_id": "ag1"})
    )
    result = calls.create_phone_call(_client(), "ag1", "+15551234567", "+15559876543")
    assert result["call_id"] == "call1"


@respx.mock
def test_create_phone_call_with_metadata():
    respx.post(f"{BASE}/create-phone-call").mock(
        return_value=httpx.Response(200, json={"call_id": "call2"})
    )
    result = calls.create_phone_call(
        _client(), "ag1", "+15551234567", "+15559876543",
        metadata='{"customer_id": "cust1"}',
    )
    assert result["call_id"] == "call2"


@respx.mock
def test_list_calls():
    respx.get(f"{BASE}/list-calls").mock(
        return_value=httpx.Response(200, json=[
            {
                "call_id": "call1", "agent_id": "ag1", "call_type": "outbound",
                "call_status": "ended", "from_number": "+1555", "to_number": "+1666",
                "start_timestamp": 1700000000, "end_timestamp": 1700000060,
                "disconnection_reason": "agent_hangup",
            }
        ])
    )
    result = calls.list_calls(_client())
    assert len(result) == 1
    assert result[0]["call_id"] == "call1"
    assert result[0]["duration_ms"] == 60


@respx.mock
def test_list_calls_no_end():
    respx.get(f"{BASE}/list-calls").mock(
        return_value=httpx.Response(200, json=[
            {"call_id": "call2", "agent_id": "ag1", "call_status": "active", "start_timestamp": 1700000000}
        ])
    )
    result = calls.list_calls(_client())
    assert result[0]["duration_ms"] is None


@respx.mock
def test_get_call():
    respx.get(f"{BASE}/get-call/call1").mock(
        return_value=httpx.Response(200, json={"call_id": "call1", "transcript": "Hello there."})
    )
    result = calls.get_call(_client(), "call1")
    assert result["call_id"] == "call1"


@respx.mock
def test_get_call_transcript():
    respx.get(f"{BASE}/get-call/call1").mock(
        return_value=httpx.Response(200, json={
            "call_id": "call1", "transcript": "Hi, how can I help?",
            "call_analysis": {"sentiment": "positive"},
            "start_timestamp": 1700000000, "end_timestamp": 1700000120,
        })
    )
    result = calls.get_call_transcript(_client(), "call1")
    assert result["call_id"] == "call1"
    assert result["transcript"] == "Hi, how can I help?"
    assert result["duration_ms"] == 120


# =============================================================================
# Phone number operations
# =============================================================================


@respx.mock
def test_list_phone_numbers():
    respx.get(f"{BASE}/list-phone-numbers").mock(
        return_value=httpx.Response(200, json=[
            {"phone_number": "+15551234567", "phone_number_pretty": "(555) 123-4567", "inbound_agent_id": "ag1", "area_code": "555", "nickname": "Main"}
        ])
    )
    result = phones.list_phone_numbers(_client())
    assert len(result) == 1
    assert result[0]["phone_number"] == "+15551234567"


@respx.mock
def test_update_phone_number():
    respx.patch(f"{BASE}/update-phone-number/+15551234567").mock(
        return_value=httpx.Response(200, json={"phone_number": "+15551234567", "nickname": "Sales Line"})
    )
    result = phones.update_phone_number(_client(), "+15551234567", nickname="Sales Line")
    assert result["nickname"] == "Sales Line"


# =============================================================================
# Voice operations
# =============================================================================


@respx.mock
def test_list_voices():
    respx.get(f"{BASE}/list-voices").mock(
        return_value=httpx.Response(200, json=[
            {"voice_id": "v1", "voice_name": "Emma", "provider": "elevenlabs", "gender": "female", "accent": "american"}
        ])
    )
    result = voices.list_voices(_client())
    assert len(result) == 1
    assert result[0]["voice_name"] == "Emma"


@respx.mock
def test_get_voice():
    respx.get(f"{BASE}/get-voice/v1").mock(
        return_value=httpx.Response(200, json={"voice_id": "v1", "voice_name": "Emma", "sample_audio_url": "https://..."})
    )
    result = voices.get_voice(_client(), "v1")
    assert result["voice_id"] == "v1"
