"""Custom tools for Deep Flo."""

from __future__ import annotations

from collections.abc import Callable
from typing import Literal

import httpx
from ddgs import DDGS
from langchain_core.tools import BaseTool, tool
from markdownify import markdownify as html_to_markdown

from deep_flo_runtime.config import DeepFloSettings


def create_runtime_tools(settings: DeepFloSettings) -> list[BaseTool | Callable]:
    """Build the custom toolset for the research runtime."""
    return [
        make_web_search_tool(settings),
        make_fetch_url_tool(settings),
    ]


def make_web_search_tool(settings: DeepFloSettings) -> BaseTool:
    """Create a web search tool with Tavily and DDGS fallback."""

    @tool
    def web_search(
        query: str,
        max_results: int = 5,
        topic: Literal["general", "news"] = "general",
    ) -> str:
        """Search the web for current information."""
        if settings.provider_status()["tavily"]:
            from tavily import TavilyClient

            client = TavilyClient()
            result = client.search(query=query, max_results=max_results, topic=topic)
            rows = []
            for item in result.get("results", []):
                rows.append(
                    "\n".join(
                        [
                            f"Title: {item.get('title', '')}",
                            f"URL: {item.get('url', '')}",
                            f"Content: {item.get('content', '')}",
                        ]
                    )
                )
            return "\n\n".join(rows) or "No search results returned."

        rows = []
        with DDGS() as client:
            for item in client.text(query, max_results=max_results):
                rows.append(
                    "\n".join(
                        [
                            f"Title: {item.get('title', '')}",
                            f"URL: {item.get('href', '')}",
                            f"Content: {item.get('body', '')}",
                        ]
                    )
                )
        return "\n\n".join(rows) or "No search results returned."

    return web_search


def make_fetch_url_tool(settings: DeepFloSettings) -> BaseTool:
    """Create a URL fetcher that returns markdown text."""

    @tool
    def fetch_url(url: str) -> str:
        """Fetch a URL and return the page as markdown-like text."""
        headers = {"User-Agent": settings.user_agent}
        with httpx.Client(timeout=settings.request_timeout_seconds, headers=headers, follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()
        content_type = response.headers.get("content-type", "")
        if "html" in content_type:
            return html_to_markdown(response.text)
        return response.text

    return fetch_url
