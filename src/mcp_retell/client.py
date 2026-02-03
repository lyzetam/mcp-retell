"""Retell AI API client with httpx support."""

from __future__ import annotations

import httpx

from mcp_retell.config import get_settings


class RetellClient:
    """Manages httpx client for Retell AI API.

    Configuration is loaded from environment variables (RETELL_* prefix)
    or a .env file via Pydantic Settings. Explicit constructor params
    override settings values.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
    ) -> None:
        settings = get_settings()
        self.api_key = (api_key or settings.api_key).strip()
        self.base_url = (base_url or settings.base_url).strip()

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    # --- Async methods (for MCP server) ---

    async def get(self, endpoint: str, params: dict | None = None) -> dict | list:
        """Make an async GET request to the Retell API."""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=30.0) as http:
            response = await http.get(endpoint, headers=self._headers(), params=params)
            response.raise_for_status()
            return response.json()

    async def post(self, endpoint: str, json: dict | None = None) -> dict:
        """Make an async POST request to the Retell API."""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=30.0) as http:
            response = await http.post(endpoint, headers=self._headers(), json=json)
            response.raise_for_status()
            return response.json()

    async def patch(self, endpoint: str, json: dict | None = None) -> dict:
        """Make an async PATCH request to the Retell API."""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=30.0) as http:
            response = await http.patch(endpoint, headers=self._headers(), json=json)
            response.raise_for_status()
            return response.json()

    async def delete(self, endpoint: str) -> dict:
        """Make an async DELETE request to the Retell API."""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=30.0) as http:
            response = await http.delete(endpoint, headers=self._headers())
            response.raise_for_status()
            return response.json()

    # --- Sync methods (for LangChain tools / operations) ---

    def get_sync(self, endpoint: str, params: dict | None = None) -> dict | list:
        """Synchronous GET for LangChain tools."""
        with httpx.Client(base_url=self.base_url, timeout=30.0) as http:
            response = http.get(endpoint, headers=self._headers(), params=params)
            response.raise_for_status()
            return response.json()

    def post_sync(self, endpoint: str, json: dict | None = None) -> dict:
        """Synchronous POST for LangChain tools."""
        with httpx.Client(base_url=self.base_url, timeout=30.0) as http:
            response = http.post(endpoint, headers=self._headers(), json=json)
            response.raise_for_status()
            return response.json()

    def patch_sync(self, endpoint: str, json: dict | None = None) -> dict:
        """Synchronous PATCH for LangChain tools."""
        with httpx.Client(base_url=self.base_url, timeout=30.0) as http:
            response = http.patch(endpoint, headers=self._headers(), json=json)
            response.raise_for_status()
            return response.json()

    def delete_sync(self, endpoint: str) -> dict:
        """Synchronous DELETE for LangChain tools."""
        with httpx.Client(base_url=self.base_url, timeout=30.0) as http:
            response = http.delete(endpoint, headers=self._headers())
            response.raise_for_status()
            return response.json()
