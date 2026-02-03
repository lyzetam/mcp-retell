"""Tests for LangChain tool interfaces."""

from langchain_core.tools import BaseTool

from mcp_retell.langchain_tools import TOOLS


def test_tools_count():
    assert len(TOOLS) == 13


def test_all_tools_are_base_tool():
    for t in TOOLS:
        assert isinstance(t, BaseTool), f"{t} is not a BaseTool"


def test_tool_names_follow_convention():
    for t in TOOLS:
        assert t.name.startswith("retell_"), f"Tool {t.name} does not follow retell_ naming convention"


def test_tool_names_are_unique():
    names = [t.name for t in TOOLS]
    assert len(names) == len(set(names)), f"Duplicate tool names: {names}"


def test_expected_tools_present():
    names = {t.name for t in TOOLS}
    expected = {
        "retell_list_agents",
        "retell_get_agent",
        "retell_create_agent",
        "retell_update_agent",
        "retell_delete_agent",
        "retell_create_phone_call",
        "retell_list_calls",
        "retell_get_call",
        "retell_get_call_transcript",
        "retell_list_phone_numbers",
        "retell_update_phone_number",
        "retell_list_voices",
        "retell_get_voice",
    }
    assert expected == names


def test_all_tools_have_descriptions():
    for t in TOOLS:
        assert t.description, f"Tool {t.name} has no description"
