"""LangChain @tool wrappers for Retell operations.

Usage:
    from mcp_retell.langchain_tools import TOOLS

    # Or import individual tools:
    from mcp_retell.langchain_tools import retell_list_agents, retell_create_phone_call
"""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Optional

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from .client import RetellClient
from .operations import agents, calls, phones, voices


@lru_cache
def _get_client() -> RetellClient:
    """Singleton RetellClient configured from environment."""
    return RetellClient()


# =============================================================================
# Agents
# =============================================================================


@tool
def retell_list_agents() -> str:
    """List all voice agents."""
    return json.dumps(agents.list_agents(_get_client()), indent=2)


class GetAgentInput(BaseModel):
    agent_id: str = Field(description="The agent ID to retrieve")


@tool(args_schema=GetAgentInput)
def retell_get_agent(agent_id: str) -> str:
    """Get details of a specific voice agent."""
    return json.dumps(agents.get_agent(_get_client(), agent_id), indent=2)


class CreateAgentInput(BaseModel):
    agent_name: str = Field(description="Name for the agent")
    voice_id: str = Field(description="Voice ID to use (from Retell voice library)")
    prompt: str = Field(description="System prompt defining agent behavior")
    language: str = Field(default="en-US", description="Language code (en-US, es-ES, etc.)")
    begin_message: Optional[str] = Field(default=None, description="Optional first message when call starts")
    model: str = Field(default="gpt-4o-mini", description="LLM model (gpt-4o-mini, gpt-4o, claude-3-5-sonnet)")
    responsiveness: float = Field(default=1.0, description="How quickly agent responds (0.0-2.0)")
    interruption_sensitivity: float = Field(default=1.0, description="Sensitivity to interruptions (0.0-2.0)")
    enable_backchannel: bool = Field(default=True, description="Enable 'uh-huh', 'I see' responses")


@tool(args_schema=CreateAgentInput)
def retell_create_agent(
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
    return json.dumps(
        agents.create_agent(
            _get_client(), agent_name, voice_id, prompt,
            language=language, begin_message=begin_message, model=model,
            responsiveness=responsiveness,
            interruption_sensitivity=interruption_sensitivity,
            enable_backchannel=enable_backchannel,
        ),
        indent=2,
    )


class UpdateAgentInput(BaseModel):
    agent_id: str = Field(description="Agent ID to update")
    agent_name: Optional[str] = Field(default=None, description="New name")
    prompt: Optional[str] = Field(default=None, description="New system prompt")
    begin_message: Optional[str] = Field(default=None, description="New begin message")
    voice_id: Optional[str] = Field(default=None, description="New voice ID")


@tool(args_schema=UpdateAgentInput)
def retell_update_agent(
    agent_id: str,
    agent_name: Optional[str] = None,
    prompt: Optional[str] = None,
    begin_message: Optional[str] = None,
    voice_id: Optional[str] = None,
) -> str:
    """Update an existing voice agent."""
    return json.dumps(
        agents.update_agent(
            _get_client(), agent_id,
            agent_name=agent_name, prompt=prompt,
            begin_message=begin_message, voice_id=voice_id,
        ),
        indent=2,
    )


class DeleteAgentInput(BaseModel):
    agent_id: str = Field(description="Agent ID to delete")


@tool(args_schema=DeleteAgentInput)
def retell_delete_agent(agent_id: str) -> str:
    """Delete a voice agent."""
    return json.dumps(agents.delete_agent(_get_client(), agent_id), indent=2)


# =============================================================================
# Calls
# =============================================================================


class CreatePhoneCallInput(BaseModel):
    agent_id: str = Field(description="Agent ID to handle the call")
    to_number: str = Field(description="Phone number to call (E.164 format: +1234567890)")
    from_number: str = Field(description="Caller ID phone number (must be registered)")
    metadata: Optional[str] = Field(default=None, description="Optional JSON metadata to attach to call")


@tool(args_schema=CreatePhoneCallInput)
def retell_create_phone_call(
    agent_id: str,
    to_number: str,
    from_number: str,
    metadata: Optional[str] = None,
) -> str:
    """Initiate an outbound phone call."""
    return json.dumps(
        calls.create_phone_call(
            _get_client(), agent_id, to_number, from_number, metadata=metadata,
        ),
        indent=2,
    )


class ListCallsInput(BaseModel):
    agent_id: Optional[str] = Field(default=None, description="Filter by agent ID")
    limit: int = Field(default=50, description="Maximum calls to return")
    sort_order: str = Field(default="descending", description="'ascending' or 'descending' by start time")


@tool(args_schema=ListCallsInput)
def retell_list_calls(
    agent_id: Optional[str] = None,
    limit: int = 50,
    sort_order: str = "descending",
) -> str:
    """List phone calls."""
    return json.dumps(
        calls.list_calls(
            _get_client(), agent_id=agent_id, limit=limit, sort_order=sort_order,
        ),
        indent=2,
    )


class GetCallInput(BaseModel):
    call_id: str = Field(description="The call ID to retrieve")


@tool(args_schema=GetCallInput)
def retell_get_call(call_id: str) -> str:
    """Get details of a specific call."""
    return json.dumps(calls.get_call(_get_client(), call_id), indent=2)


class GetCallTranscriptInput(BaseModel):
    call_id: str = Field(description="The call ID to get transcript for")


@tool(args_schema=GetCallTranscriptInput)
def retell_get_call_transcript(call_id: str) -> str:
    """Get the transcript of a call."""
    return json.dumps(calls.get_call_transcript(_get_client(), call_id), indent=2)


# =============================================================================
# Phone Numbers
# =============================================================================


@tool
def retell_list_phone_numbers() -> str:
    """List all registered phone numbers."""
    return json.dumps(phones.list_phone_numbers(_get_client()), indent=2)


class UpdatePhoneNumberInput(BaseModel):
    phone_number: str = Field(description="Phone number to update (E.164 format)")
    inbound_agent_id: Optional[str] = Field(default=None, description="Agent to handle inbound calls")
    nickname: Optional[str] = Field(default=None, description="Friendly name for the number")


@tool(args_schema=UpdatePhoneNumberInput)
def retell_update_phone_number(
    phone_number: str,
    inbound_agent_id: Optional[str] = None,
    nickname: Optional[str] = None,
) -> str:
    """Update a phone number configuration."""
    return json.dumps(
        phones.update_phone_number(
            _get_client(), phone_number,
            inbound_agent_id=inbound_agent_id, nickname=nickname,
        ),
        indent=2,
    )


# =============================================================================
# Voices
# =============================================================================


@tool
def retell_list_voices() -> str:
    """List available voices from Retell's voice library."""
    return json.dumps(voices.list_voices(_get_client()), indent=2)


class GetVoiceInput(BaseModel):
    voice_id: str = Field(description="Voice ID to retrieve")


@tool(args_schema=GetVoiceInput)
def retell_get_voice(voice_id: str) -> str:
    """Get details of a specific voice."""
    return json.dumps(voices.get_voice(_get_client(), voice_id), indent=2)


# =============================================================================
# Tool exports
# =============================================================================

TOOLS = [
    # Agents
    retell_list_agents,
    retell_get_agent,
    retell_create_agent,
    retell_update_agent,
    retell_delete_agent,
    # Calls
    retell_create_phone_call,
    retell_list_calls,
    retell_get_call,
    retell_get_call_transcript,
    # Phone Numbers
    retell_list_phone_numbers,
    retell_update_phone_number,
    # Voices
    retell_list_voices,
    retell_get_voice,
]
